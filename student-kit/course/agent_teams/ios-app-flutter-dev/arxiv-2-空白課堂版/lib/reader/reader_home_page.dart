/// 報告閱讀模組 —— reader-owner 擁有並維護。
///
/// 對外只 export [ReaderHomePage](無必填建構參數)。
/// 資料透過共用層 [ReportApiClient] 取得，不直接碰 http / jsonDecode。
/// team lead 整合時會在 lib/main.dart 用：
///   home: BreathingReminderScope(child: ReaderHomePage())
library;

import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:url_launcher/url_launcher.dart';

import '../shared/models.dart';
import '../shared/report_api_client.dart';

/// 今日報告閱讀首頁。
///
/// - 載入中：顯示 CircularProgressIndicator
/// - 錯誤(含 404 無報告)：顯示友善訊息
/// - 成功：render markdown 報告 + 固定 5 篇 papers 清單(有頂有底)
///
/// AppBar 右側有歷史 icon，點擊開 bottom sheet 讓使用者選舊報告日期。
///
/// [client] 選填：測試時注入 mock client，正式執行不傳即用預設。
/// 無必填建構參數 —— 符合 api-contract.md 第 3 節 widget 交接介面。
class ReaderHomePage extends StatefulWidget {
  final ReportApiClient? client;

  const ReaderHomePage({super.key, this.client});

  @override
  State<ReaderHomePage> createState() => _ReaderHomePageState();
}

class _ReaderHomePageState extends State<ReaderHomePage> {
  late final ReportApiClient _client;

  // 當前顯示的報告(null = 尚未載入或錯誤)
  Report? _report;
  bool _loading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _client = widget.client ?? ReportApiClient();
    _loadTodayReport();
  }

  @override
  void dispose() {
    _client.close();
    super.dispose();
  }

  // ── 資料載入 ──────────────────────────────────────────────

  Future<void> _loadTodayReport() async {
    setState(() {
      _loading = true;
      _errorMessage = null;
    });
    try {
      final report = await _client.today();
      setState(() {
        _report = report;
        _loading = false;
      });
    } on ReportApiException catch (e) {
      setState(() {
        _loading = false;
        _errorMessage = e.statusCode == 404
            ? '今日報告尚未產生，請稍後再試。'
            : '無法取得今日報告，請確認網路連線。\n(錯誤：${e.message})';
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _errorMessage = '連不上後端，請確認 App 與後端是否同時執行。';
      });
    }
  }

  Future<void> _loadReportByDate(String date) async {
    setState(() {
      _loading = true;
      _errorMessage = null;
    });
    try {
      final report = await _client.byDate(date);
      setState(() {
        _report = report;
        _loading = false;
      });
    } on ReportApiException catch (e) {
      setState(() {
        _loading = false;
        _errorMessage = e.statusCode == 404
            ? '$date 的報告不存在。'
            : '無法載入 $date 的報告。\n(錯誤：${e.message})';
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _errorMessage = '載入失敗，請確認網路連線。';
      });
    }
  }

  // ── 歷史日期選擇 ──────────────────────────────────────────

  Future<void> _showHistorySheet() async {
    List<String>? dates;
    String? fetchError;

    try {
      dates = await _client.list();
    } on ReportApiException catch (e) {
      fetchError = '無法取得歷史清單：${e.message}';
    } catch (e) {
      fetchError = '連線失敗，無法載入歷史清單。';
    }

    if (!mounted) return;

    showModalBottomSheet<void>(
      context: context,
      builder: (ctx) {
        if (fetchError != null) {
          return Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.error_outline, color: Colors.red, size: 40),
                const SizedBox(height: 12),
                Text(fetchError, textAlign: TextAlign.center),
              ],
            ),
          );
        }
        if (dates == null || dates.isEmpty) {
          return const Padding(
            padding: EdgeInsets.all(24),
            child: Text('目前沒有歷史報告。', textAlign: TextAlign.center),
          );
        }
        return Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 12),
              child: Text(
                '選擇歷史日期',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
            const Divider(height: 1),
            Flexible(
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: dates.length,
                separatorBuilder: (_, __) => const Divider(height: 1),
                itemBuilder: (_, i) {
                  final date = dates![i];
                  return ListTile(
                    leading: const Icon(Icons.calendar_today, size: 18),
                    title: Text(date),
                    onTap: () {
                      Navigator.of(ctx).pop();
                      _loadReportByDate(date);
                    },
                  );
                },
              ),
            ),
            const SizedBox(height: 8),
          ],
        );
      },
    );
  }

  // ── UI ───────────────────────────────────────────────────

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_report?.date != null ? _report!.date : 'arXiv 每日論文'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            tooltip: '歷史報告',
            onPressed: _showHistorySheet,
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: '重新載入',
            onPressed: _loadTodayReport,
          ),
        ],
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_errorMessage != null) {
      return _ErrorView(
        message: _errorMessage!,
        onRetry: _loadTodayReport,
      );
    }
    if (_report == null) {
      return const Center(child: Text('尚無報告資料'));
    }
    return _ReportView(report: _report!);
  }
}

// ── 子 Widget ──────────────────────────────────────────────

/// 錯誤狀態畫面。
class _ErrorView extends StatelessWidget {
  final String message;
  final VoidCallback onRetry;

  const _ErrorView({required this.message, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.cloud_off, size: 56, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              message,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('重新載入今日報告'),
            ),
          ],
        ),
      ),
    );
  }
}

/// 報告內容畫面（Markdown 本文 + 固定 5 篇論文清單）。
///
/// 設計紅線：固定清單有頂有底，不做無限滑、不自動播下一篇。
class _ReportView extends StatelessWidget {
  final Report report;

  const _ReportView({required this.report});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // ── 報告標題 ────────────────────────────────────────
        Container(
          color: Theme.of(context).colorScheme.primaryContainer,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          child: Text(
            report.title,
            style: TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.onPrimaryContainer,
            ),
          ),
        ),

        // ── Markdown 報告本文（可捲動，有頂有底）──────────────
        Expanded(
          child: Markdown(
            data: report.markdownBody,
            selectable: true,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            onTapLink: (text, href, title) {
              if (href != null) _launchUrl(href);
            },
          ),
        ),

        // ── 論文清單分隔線 ──────────────────────────────────
        const Divider(height: 1),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            '本期論文（${report.papers.length} 篇）',
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.bold,
              color: Colors.grey,
            ),
          ),
        ),

        // ── 固定 5 篇論文清單（有頂有底，不無限滑）───────────
        _PaperList(papers: report.papers),
      ],
    );
  }

  void _launchUrl(String url) async {
    final uri = Uri.tryParse(url);
    if (uri != null && await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }
}

/// 固定 5 篇論文的清單，每項顯示標題、作者、arXiv 連結。
///
/// 設計紅線：有頂有底（shrinkWrap + NeverScrollableScrollPhysics），
/// 整體捲動由外層 Column 的 Markdown 區塊承擔；不做無限滑。
class _PaperList extends StatelessWidget {
  final List<Paper> papers;

  const _PaperList({required this.papers});

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: papers.length,
      separatorBuilder: (_, __) => const Divider(height: 1, indent: 16),
      itemBuilder: (context, index) => _PaperTile(paper: papers[index]),
    );
  }
}

/// 單篇論文的清單項目。
class _PaperTile extends StatelessWidget {
  final Paper paper;

  const _PaperTile({required this.paper});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 標題
          Text(
            paper.title,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 4),
          // 作者
          Text(
            paper.authorsLine,
            style: const TextStyle(
              fontSize: 12,
              color: Colors.grey,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 6),
          // arXiv 連結
          InkWell(
            onTap: () => _launchArxiv(paper.link),
            child: Text(
              paper.link,
              style: TextStyle(
                fontSize: 12,
                color: Theme.of(context).colorScheme.primary,
                decoration: TextDecoration.underline,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _launchArxiv(String url) async {
    final uri = Uri.tryParse(url);
    if (uri != null && await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }
}
