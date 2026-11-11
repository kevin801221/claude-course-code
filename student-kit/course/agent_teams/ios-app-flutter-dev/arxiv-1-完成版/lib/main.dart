import 'package:flutter/material.dart';

import 'breathing/breathing_reminder_scope.dart';
import 'reader/reader_home_page.dart';

void main() {
  runApp(const ArxivReaderApp());
}

/// App 進入點 + 首頁路由(team lead 擁有的共用層)。
///
/// 組裝方式由 API 契約凍結(見 _Context/api-contract.md):
/// 閱讀內容(reader)被呼吸提醒範圍(breathing)包住,讀久了自動跳呼吸動畫。
class ArxivReaderApp extends StatelessWidget {
  const ArxivReaderApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'arXiv 每日論文閱讀器',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF1E2761),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: const BreathingReminderScope(
        threshold: Duration(seconds: 90), // demo 用,正式應移除(預設 10 分鐘)
        child: ReaderHomePage(),
      ),
    );
  }
}
