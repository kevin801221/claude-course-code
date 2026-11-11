/// 共用資料模型 —— 對應 team lead 凍結的 API 契約(見 _Context/api-contract.md)。
///
/// 共用層由 team lead 擁有與凍結。隊友(reader-owner / breathing-owner /
/// backend-owner)要改這裡的欄位,請先用 mailbox 問 team lead、等批准,不要自己改。
library;

/// 一篇 arXiv 論文。對應契約 papers[] 的元素。
class Paper {
  final String title;
  final List<String> authors;
  final String arxivId;
  final String link;
  final String summary;

  const Paper({
    required this.title,
    required this.authors,
    required this.arxivId,
    required this.link,
    required this.summary,
  });

  factory Paper.fromJson(Map<String, dynamic> json) {
    return Paper(
      title: (json['title'] ?? '').toString(),
      authors: _parseAuthors(json['authors']),
      arxivId: (json['arxivId'] ?? '').toString(),
      link: (json['link'] ?? '').toString(),
      summary: (json['summary'] ?? '').toString(),
    );
  }

  Map<String, dynamic> toJson() => {
        'title': title,
        'authors': authors,
        'arxivId': arxivId,
        'link': link,
        'summary': summary,
      };

  /// 後端可能回傳 List 或逗號分隔字串,兩種都容錯。
  static List<String> _parseAuthors(dynamic raw) {
    if (raw is List) {
      return raw.map((e) => e.toString()).toList();
    }
    if (raw is String && raw.trim().isNotEmpty) {
      return raw.split(',').map((e) => e.trim()).toList();
    }
    return const [];
  }
}

/// 一份每日研究報告。對應契約 GET /reports/today 的回傳。
class Report {
  final String date; // YYYY-MM-DD
  final String title;
  final String markdownBody;
  final List<Paper> papers;

  const Report({
    required this.date,
    required this.title,
    required this.markdownBody,
    required this.papers,
  });

  factory Report.fromJson(Map<String, dynamic> json) {
    final rawPapers = json['papers'];
    return Report(
      date: (json['date'] ?? '').toString(),
      title: (json['title'] ?? '').toString(),
      markdownBody: (json['markdownBody'] ?? '').toString(),
      papers: rawPapers is List
          ? rawPapers
              .whereType<Map>()
              .map((e) => Paper.fromJson(Map<String, dynamic>.from(e)))
              .toList()
          : const [],
    );
  }

  Map<String, dynamic> toJson() => {
        'date': date,
        'title': title,
        'markdownBody': markdownBody,
        'papers': papers.map((p) => p.toJson()).toList(),
      };
}
