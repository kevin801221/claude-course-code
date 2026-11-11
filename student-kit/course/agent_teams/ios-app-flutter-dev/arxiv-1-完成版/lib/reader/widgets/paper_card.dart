import 'package:flutter/material.dart';

import '../../shared/models.dart';

/// 單篇論文卡片:標題 / 作者 / 摘要 / arXiv 連結。
///
/// arXiv 連結用 [SelectableText] 顯示 URL(可長按複製);
/// 若日後要點擊開外部瀏覽器需 `url_launcher` 套件 → 先 mailbox 問 team lead。
class PaperCard extends StatelessWidget {
  final Paper paper;

  const PaperCard({super.key, required this.paper});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              paper.title,
              style: theme.textTheme.titleSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
            if (paper.authors.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text(
                paper.authors.join(', '),
                style: theme.textTheme.bodySmall?.copyWith(
                  color: theme.colorScheme.outline,
                ),
              ),
            ],
            if (paper.summary.trim().isNotEmpty) ...[
              const SizedBox(height: 8),
              Text(paper.summary, style: theme.textTheme.bodyMedium),
            ],
            if (paper.link.isNotEmpty) ...[
              const SizedBox(height: 10),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.link, size: 16, color: theme.colorScheme.primary),
                  const SizedBox(width: 4),
                  Expanded(
                    child: SelectableText(
                      paper.link,
                      style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.primary,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
