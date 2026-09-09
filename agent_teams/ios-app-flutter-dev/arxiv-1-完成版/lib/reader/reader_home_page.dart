import 'package:flutter/material.dart';

import 'report_screen.dart';

/// 報告閱讀首頁(模組 B,reader-owner 擁有)。
///
/// 這是 main.dart 組裝用的 public 入口 —— **簽章維持 team lead 凍結的樣子**
/// (`const ReaderHomePage({super.key})`),真正的畫面邏輯放在 [ReportScreen]。
///
/// 設計紅線(來自研究結論,見 _Context/app-spec.md):
///   - 每日固定 5 篇、有明確結尾
///   - 不做無限滑 / 紅點未讀數字 / 罪惡感文案
class ReaderHomePage extends StatelessWidget {
  const ReaderHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return const ReportScreen();
  }
}
