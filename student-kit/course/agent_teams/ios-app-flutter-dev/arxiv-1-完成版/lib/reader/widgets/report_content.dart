import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

import '../../shared/models.dart';
import 'paper_card.dart';

/// 一份報告的閱讀內容:標題 + 日期 + markdown 綜述 + papers 清單 + 明確結尾。
///
/// 用 [ListView] 呈現固定長度內容(每日 5 篇、讀完就結束)——
/// **刻意不做無限滑 / 未讀數字**(設計紅線)。
class ReportContent extends StatelessWidget {
  final Report report;

  /// 下拉重新整理 / 重新拉當前報告。
  final Future<void> Function() onRefresh;

  const ReportContent({
    super.key,
    required this.report,
    required this.onRefresh,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final hasMarkdown = report.markdownBody.trim().isNotEmpty;

    return RefreshIndicator(
      onRefresh: onRefresh,
      child: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 40),
        children: [
          Text(report.title, style: theme.textTheme.headlineSmall),
          const SizedBox(height: 4),
          Text(
            report.date,
            style: theme.textTheme.labelMedium?.copyWith(
              color: theme.colorScheme.outline,
            ),
          ),
          const Divider(height: 28),
          if (hasMarkdown)
            MarkdownBody(
              data: report.markdownBody,
              selectable: true,
            ),
          const SizedBox(height: 24),
          Text(
            '今日 ${report.papers.length} 篇論文',
            style: theme.textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          if (report.papers.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16),
              child: Text(
                '今日沒有論文資料。',
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: theme.colorScheme.outline,
                ),
              ),
            )
          else
            ...report.papers.map((paper) => PaperCard(paper: paper)),
          const SizedBox(height: 28),
          // 明確結尾:讀完就是讀完,不引導繼續無限滑。
          Center(
            child: Text(
              '— 今天讀完了,明天見 —',
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.colorScheme.outline,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
