// 濾波與告警單元測試：test_filters <case>；Release 有 NDEBUG，所以用自訂 CHECK 而非 assert。
#include "filters.hpp"

#include <cmath>
#include <cstdio>
#include <functional>
#include <map>
#include <string>

using wb::Opt;

static int g_fail = 0;
#define CHECK(cond) do { if (!(cond)) { std::printf("FAIL %s:%d: %s\n", __FILE__, __LINE__, #cond); ++g_fail; } } while (0)

static bool near(Opt y, double v, double tol = 1e-12) { return y && std::fabs(*y - v) <= tol; }

static void constant_unchanged() {
    for (const char* m : {"sma", "ema", "median"}) {
        auto f = wb::make_filter(m, 5, 0.3);
        for (int i = 0; i < 20; ++i) CHECK(near(f->step(38.07), 38.07));
        auto g = wb::make_filter(m, 5, 0.3);
        for (int i = 0; i < 20; ++i) { auto y = g->step(45.0); CHECK(y && *y == 45.0); }
    }
}

static void median_sort_even() {
    wb::Median m(5);
    CHECK(near(m.step(3), 3));
    CHECK(near(m.step(1), 2));      // {1,3} 偶數 → 平均
    CHECK(near(m.step(2), 2));      // {1,2,3}
    CHECK(near(m.step(4), 2.5));    // {1,2,3,4} → (2+3)/2
    CHECK(near(m.step(9), 3));      // {1,2,3,4,9}
    CHECK(near(m.step(0), 2));      // 視窗滑動：{1,2,4,9,0} → 2
}

static void ema_first_sample() {
    wb::Ema e(0.3);
    CHECK(near(e.step(10), 10));     // 第一筆有效樣本直接初始化
    CHECK(near(e.step(20), 13));     // 10 + 0.3*(20-10)
    CHECK(near(e.step(20), 15.1));   // 13 + 0.3*(20-13)
}

static void startup_partial_window() {
    wb::Sma s(5);
    CHECK(near(s.step(1), 1));
    CHECK(near(s.step(2), 1.5));
    CHECK(near(s.step(3), 2));
    CHECK(near(s.step(4), 2.5));
    CHECK(near(s.step(5), 3));
    CHECK(near(s.step(6), 4));       // 視窗 {2..6}
}

static void threshold_equal_third() {
    wb::Alarm a(45.0, 3);
    a.step(44.99);
    CHECK(!a.active());
    a.step(45.0); CHECK(!a.active());
    a.step(45.0); CHECK(!a.active());
    a.step(45.0); CHECK(a.active());  // 等於門檻的第三筆觸發
    wb::Sma s(5);
    wb::Alarm b(45.0, 3);
    for (int i = 0; i < 2; ++i) { b.step(s.step(45.0)); CHECK(!b.active()); }
    b.step(s.step(45.0)); CHECK(b.active());
}

static void missing_resets() {
    for (const char* m : {"sma", "ema", "median"}) {
        auto f = wb::make_filter(m, 5, 0.3);
        f->step(10); f->step(20);
        CHECK(!f->step(std::nullopt));     // 缺測輸出空值，不當 0
        CHECK(near(f->step(30), 30));      // 重新初始化，不混入舊樣本
    }
    wb::Alarm a(45.0, 3);
    a.step(46); a.step(46); a.step(std::nullopt);
    CHECK(!a.active());
    a.step(46); a.step(46); CHECK(!a.active());
    a.step(46); CHECK(a.active());
    a.step(std::nullopt); CHECK(!a.active());
}

static void isolated_spike_no_trigger() {
    wb::Alarm raw(45.0, 3);
    for (double v : {40.0, 40.0, 60.0, 40.0, 40.0}) { raw.step(v); CHECK(!raw.active()); }
    wb::Median m(5);
    wb::Alarm a(45.0, 3);
    for (int i = 0; i < 12; ++i) {
        a.step(m.step(i == 6 ? 70.0 : 40.0));
        CHECK(!a.active());
    }
}

static void sustained_rise_triggers() {
    for (const char* m : {"sma", "ema", "median"}) {
        auto f = wb::make_filter(m, 5, 0.3);
        wb::Alarm a(45.0, 3);
        bool fired = false;
        for (int i = 0; i <= 40; ++i) { a.step(f->step(40.0 + 0.5 * i)); fired = fired || a.active(); }
        CHECK(fired);
    }
}

int main(int argc, char** argv) {
    const std::map<std::string, std::function<void()>> cases = {
        {"constant_unchanged", constant_unchanged},
        {"median_sort_even", median_sort_even},
        {"ema_first_sample", ema_first_sample},
        {"startup_partial_window", startup_partial_window},
        {"threshold_equal_third", threshold_equal_third},
        {"missing_resets", missing_resets},
        {"isolated_spike_no_trigger", isolated_spike_no_trigger},
        {"sustained_rise_triggers", sustained_rise_triggers},
    };
    if (argc != 2 || !cases.count(argv[1])) { std::printf("unknown case\n"); return 2; }
    cases.at(argv[1])();
    std::printf("%s: %s\n", argv[1], g_fail ? "FAIL" : "ok");
    return g_fail ? 1 : 0;
}
