/// App 進入點 + 首頁路由 —— team lead 擁有的共用層。
///
/// 目前 reader / breathing 模組由隊友平行開發中；整合階段(task #6)
/// team lead 會把首頁換成 reader 的 `ReaderHomePage`，外層包 breathing 的
/// `BreathingReminderScope`(widget 交接介面見 `_Context/api-contract.md` 第 3 節)。
library;

import 'package:flutter/material.dart';

void main() {
  runApp(const ArxivReaderApp());
}

class ArxivReaderApp extends StatelessWidget {
  const ArxivReaderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'arXiv 每日論文閱讀器',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF1E2761)),
        useMaterial3: true,
      ),
      // 整合時換成：BreathingReminderScope(child: ReaderHomePage())
      home: const _ScaffoldPlaceholder(),
    );
  }
}

/// 共用層完成、等三模組整合時的暫時首頁。整合階段會被 ReaderHomePage 取代。
class _ScaffoldPlaceholder extends StatelessWidget {
  const _ScaffoldPlaceholder();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('arXiv 每日論文閱讀器')),
      body: const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Text(
            '共用層(lib/shared)已就緒。\n'
            'reader / breathing 模組整合後，此頁將換成報告閱讀畫面。',
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }
}
