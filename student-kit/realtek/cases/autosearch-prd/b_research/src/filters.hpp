// 三個候選濾波器（SMA／EMA／Median）與共用告警器。
// 約定：輸入 nullopt 代表缺測 → 輸出 nullopt 並重置狀態；下一筆有效值重新初始化。
#pragma once
#include <algorithm>
#include <deque>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

namespace wb {

using Opt = std::optional<double>;

struct Filter {
    virtual ~Filter() = default;
    virtual Opt step(Opt x) = 0;
};

// SMA／Median 共用：近 n 筆「實有、含當筆」樣本，啟動期用已有的樣本。
class WindowFilter : public Filter {
public:
    explicit WindowFilter(std::size_t n) : n_(n) {
        if (n == 0) throw std::invalid_argument("window must be >= 1");
    }
    Opt step(Opt x) override {
        if (!x) { w_.clear(); return std::nullopt; }
        w_.push_back(*x);
        if (w_.size() > n_) w_.pop_front();
        return reduce();
    }
protected:
    virtual double reduce() const = 0;
    std::size_t n_;
    std::deque<double> w_;
};

class Sma : public WindowFilter {
public:
    using WindowFilter::WindowFilter;
protected:
    double reduce() const override {
        double s = 0.0;  // 每步重算（n=5），避免累加誤差漂移
        for (double v : w_) s += v;
        return s / static_cast<double>(w_.size());
    }
};

class Median : public WindowFilter {
public:
    using WindowFilter::WindowFilter;
protected:
    double reduce() const override {
        std::vector<double> v(w_.begin(), w_.end());
        std::sort(v.begin(), v.end());
        const std::size_t m = v.size() / 2;
        return v.size() % 2 ? v[m] : (v[m - 1] + v[m]) / 2.0;  // 偶數取中間兩筆平均
    }
};

class Ema : public Filter {
public:
    explicit Ema(double alpha) : a_(alpha) {
        if (!(alpha > 0.0 && alpha <= 1.0)) throw std::invalid_argument("alpha must be in (0,1]");
    }
    Opt step(Opt x) override {
        if (!x) { init_ = false; return std::nullopt; }
        if (!init_) { y_ = *x; init_ = true; }  // 第一筆有效樣本初始化
        else y_ += a_ * (*x - y_);             // 常數輸入時位元級不變
        return y_;
    }
private:
    double a_;
    double y_ = 0.0;
    bool init_ = false;
};

// 濾波輸出 >= threshold 連續 need 筆才告警（第 need 筆觸發）；低於門檻或缺值即重置。
class Alarm {
public:
    Alarm(double threshold, int need) : thr_(threshold), need_(need) {}
    int step(Opt y) {
        if (!y || *y < thr_) count_ = 0;
        else ++count_;
        return count_;
    }
    bool active() const { return count_ >= need_; }
private:
    double thr_;
    int need_;
    int count_ = 0;
};

inline std::unique_ptr<Filter> make_filter(const std::string& method, std::size_t window, double alpha) {
    if (method == "sma") return std::make_unique<Sma>(window);
    if (method == "median") return std::make_unique<Median>(window);
    if (method == "ema") return std::make_unique<Ema>(alpha);
    throw std::invalid_argument("unknown method: " + method);
}

}  // namespace wb
