#include <emscripten/bind.h>
#include <cmath>
#include <string>
#include <sstream>
#include <iomanip>

using namespace emscripten;

// 入力はミリ秒（double）を想定
// 戻り値はミリ秒差（実際の経過 - 10000）。正なら遅い（遅れ）、負なら早い（早かった）
double compute_offset_ms(double start_ms, double stop_ms) {
    double elapsed = stop_ms - start_ms;
    return elapsed - 10000.0; // 10秒 = 10000 ms
}

// 誤差の表現を返す（フォーマット済み文字列）
// 例: "+123.45 ms (1.23% slow)" または "-87.65 ms (0.88% fast)"
std::string format_result(double offset_ms) {
    double abs_ms = std::abs(offset_ms);
    double pct = (abs_ms / 10000.0) * 100.0;
    std::ostringstream ss;
    ss << std::fixed << std::setprecision(2);
    if (offset_ms > 0) {
        ss << "+" << abs_ms << " ms (" << pct << "% slow)";
    } else if (offset_ms < 0) {
        ss << "-" << abs_ms << " ms (" << pct << "% fast)";
    } else {
        ss << "Perfect! 0.00 ms (0.00% )";
    }
    return ss.str();
}

EMSCRIPTEN_BINDINGS(timer_module) {
    function("compute_offset_ms", &compute_offset_ms);
    function("format_result", &format_result);
}
