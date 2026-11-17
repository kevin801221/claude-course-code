// wb_filter：讀 timestamp_s,temp_c（1 Hz、嚴格遞增、空值=缺測），輸出逐筆濾波與告警。
//   wb_filter run   --method sma|ema|median --in raw.csv --out rows.csv [--window 5 --alpha 0.3 --threshold 45 --consecutive 3]
//   wb_filter bench --method ... --in raw.csv [--samples 100000 --warmup 3 --trials 15]
//   wb_filter info
#include "filters.hpp"

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>

#ifndef WB_CXX_ID
#define WB_CXX_ID "unknown"
#endif
#ifndef WB_CXX_VERSION
#define WB_CXX_VERSION "unknown"
#endif
#ifndef WB_BUILD_TYPE
#define WB_BUILD_TYPE "unknown"
#endif
#ifndef WB_CXX_FLAGS
#define WB_CXX_FLAGS "unknown"
#endif

namespace {

struct Row { long t; wb::Opt v; std::string text; };  // text：原樣回寫輸入值

[[noreturn]] void die(const std::string& msg) {
    std::cerr << "錯誤：" << msg << "\n";
    std::exit(1);
}

std::vector<std::string> split(const std::string& s) {
    std::vector<std::string> out;
    std::string cur;
    std::istringstream in(s);
    while (std::getline(in, cur, ',')) out.push_back(cur);
    if (!s.empty() && s.back() == ',') out.emplace_back();
    return out;
}

bool parse_double(const std::string& s, double& out) {
    if (s.empty()) return false;
    char* end = nullptr;
    out = std::strtod(s.c_str(), &end);
    return end == s.c_str() + s.size() && std::isfinite(out);
}

std::vector<Row> read_csv(const std::string& path) {
    std::ifstream f(path);
    if (!f) die("無法開啟輸入檔 " + path);
    std::string line;
    if (!std::getline(f, line)) die("輸入檔是空的：" + path);
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.rfind("\xEF\xBB\xBF", 0) == 0) line.erase(0, 3);
    auto head = split(line);
    int it = -1, iv = -1;
    for (int i = 0; i < static_cast<int>(head.size()); ++i) {
        if (head[i] == "timestamp_s") it = i;
        if (head[i] == "temp_c") iv = i;
    }
    if (it < 0) die("缺少欄位：timestamp_s");
    if (iv < 0) die("缺少欄位：temp_c");
    std::vector<Row> rows;
    long lineno = 1;
    while (std::getline(f, line)) {
        ++lineno;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (line.empty()) continue;
        auto c = split(line);
        if (c.size() != head.size()) die("第 " + std::to_string(lineno) + " 行欄位數不符");
        double t;
        if (!parse_double(c[it], t) || t != std::floor(t)) die("第 " + std::to_string(lineno) + " 行 timestamp_s 不是整數秒");
        Row r{static_cast<long>(t), std::nullopt, c[iv]};
        if (!rows.empty() && r.t != rows.back().t + 1)
            die("第 " + std::to_string(lineno) + " 行時間戳必須嚴格遞增且每秒一筆（1 Hz）");
        double v;
        if (!c[iv].empty()) {
            if (!parse_double(c[iv], v)) die("第 " + std::to_string(lineno) + " 行 temp_c 不是數值");
            r.v = v;
        }
        rows.push_back(r);
    }
    if (rows.empty()) die("輸入檔沒有資料列：" + path);
    return rows;
}

std::map<std::string, std::string> parse_opts(int argc, char** argv) {
    std::map<std::string, std::string> o;
    for (int i = 2; i < argc; ++i) {
        std::string k = argv[i];
        if (k.rfind("--", 0) != 0 || i + 1 >= argc) die("參數格式錯誤：" + k);
        o[k.substr(2)] = argv[++i];
    }
    return o;
}

std::string need(const std::map<std::string, std::string>& o, const std::string& k) {
    auto it = o.find(k);
    if (it == o.end()) die("缺少參數 --" + k);
    return it->second;
}

double num(const std::map<std::string, std::string>& o, const std::string& k, double dflt) {
    auto it = o.find(k);
    if (it == o.end()) return dflt;
    double v;
    if (!parse_double(it->second, v)) die("參數 --" + k + " 不是數值");
    return v;
}

int cmd_run(const std::map<std::string, std::string>& o) {
    auto rows = read_csv(need(o, "in"));
    auto f = wb::make_filter(need(o, "method"), static_cast<std::size_t>(num(o, "window", 5)), num(o, "alpha", 0.3));
    wb::Alarm alarm(num(o, "threshold", 45.0), static_cast<int>(num(o, "consecutive", 3)));
    std::ofstream out(need(o, "out"), std::ios::binary);
    if (!out) die("無法寫入輸出檔");
    out << "timestamp_s,temp_c,filtered_c,consecutive,alarm\n";
    char buf[64];
    for (const auto& r : rows) {
        wb::Opt y = f->step(r.v);
        int cnt = alarm.step(y);
        out << r.t << ',' << r.text << ',';
        if (y) { std::snprintf(buf, sizeof buf, "%.17g", *y); out << buf; }
        out << ',' << cnt << ',' << (alarm.active() ? 1 : 0) << '\n';
    }
    return out ? 0 : 1;
}

int cmd_bench(const std::map<std::string, std::string>& o) {
    auto rows = read_csv(need(o, "in"));
    const std::string method = need(o, "method");
    const auto n = static_cast<std::size_t>(num(o, "samples", 100000));
    const int warmup = static_cast<int>(num(o, "warmup", 3));
    const int trials = static_cast<int>(num(o, "trials", 15));
    const auto window = static_cast<std::size_t>(num(o, "window", 5));
    const double alpha = num(o, "alpha", 0.3);
    std::vector<wb::Opt> xs(n);
    for (std::size_t i = 0; i < n; ++i) xs[i] = rows[i % rows.size()].v;  // 先載入記憶體，不計 I/O
    std::vector<double> ns;
    double checksum = 0.0;  // 累加輸出並印出，避免編譯器把工作消掉
    for (int k = 0; k < warmup + trials; ++k) {
        auto f = wb::make_filter(method, window, alpha);
        double sink = 0.0;
        auto t0 = std::chrono::steady_clock::now();
        for (const auto& x : xs) { auto y = f->step(x); if (y) sink += *y; }
        auto t1 = std::chrono::steady_clock::now();
        checksum += sink;
        if (k >= warmup)
            ns.push_back(std::chrono::duration<double, std::nano>(t1 - t0).count() / static_cast<double>(n));
    }
    std::vector<double> sorted = ns;
    std::sort(sorted.begin(), sorted.end());
    const std::size_t m = sorted.size() / 2;
    const double med = sorted.size() % 2 ? sorted[m] : (sorted[m - 1] + sorted[m]) / 2.0;
    std::printf("{\"method\":\"%s\",\"samples\":%zu,\"warmup\":%d,\"trials\":%d,"
                "\"ns_per_sample_median\":%.4f,\"ns_per_sample_min\":%.4f,\"ns_per_sample_max\":%.4f,"
                "\"checksum\":%.6f,\"timer\":\"std::chrono::steady_clock\",\"scope\":\"filter step only, no I/O\"}\n",
                method.c_str(), n, warmup, trials, med, sorted.front(), sorted.back(), checksum);
    return 0;
}

int cmd_info() {
    std::printf("{\"compiler_id\":\"%s\",\"compiler_version\":\"%s\",\"build_type\":\"%s\",\"cxx_flags\":\"%s\",\"cxx_standard\":%ld}\n",
                WB_CXX_ID, WB_CXX_VERSION, WB_BUILD_TYPE, WB_CXX_FLAGS, static_cast<long>(__cplusplus));
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) die("用法：wb_filter run|bench|info ...");
    const std::string cmd = argv[1];
    try {
        if (cmd == "run") return cmd_run(parse_opts(argc, argv));
        if (cmd == "bench") return cmd_bench(parse_opts(argc, argv));
        if (cmd == "info") return cmd_info();
    } catch (const std::exception& e) {
        die(e.what());
    }
    die("未知指令：" + cmd);
}
