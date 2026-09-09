import 'package:flutter/material.dart';

import '../shared/models.dart';
import '../shared/report_api_client.dart';
import 'widgets/report_content.dart';

/// 載入狀態機:轉圈 / 友善空狀態 / 錯誤可重試 / 報告內容。
enum _LoadState { loading, empty, error, data }

/// 報告閱讀畫面(reader-owner 擁有的真實作)。
///
/// - 用共用層 [ReportApiClient] 拉今日報告 + 歷史清單(不自己寫 http / jsonDecode)
/// - render `markdownBody`、列出 papers、提供歷史回看
/// - 處理 loading / empty(404)/ error(可重試)三種非資料狀態
///
/// 測試可注入 [client](fake / mock);正式使用走預設 [ReportApiClient]。
class ReportScreen extends StatefulWidget {
  final ReportApiClient? client;

  const ReportScreen({super.key, this.client});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  late final ReportApiClient _client;
  bool _ownsClient = false;

  _LoadState _state = _LoadState.loading;
  Report? _report;
  String _message = '';

  /// null = 今天;非 null = 正在看的歷史日期。
  String? _selectedDate;

  @override
  void initState() {
    super.initState();
    if (widget.client != null) {
      _client = widget.client!;
    } else {
      _client = ReportApiClient();
      _ownsClient = true;
    }
    _loadToday();
  }

  @override
  void dispose() {
    if (_ownsClient) {
      _client.dispose();
    }
    super.dispose();
  }

  Future<void> _loadToday() async {
    setState(() {
      _state = _LoadState.loading;
      _selectedDate = null;
    });
    await _load(() => _client.today());
  }

  Future<void> _loadDate(String date) async {
    setState(() {
      _state = _LoadState.loading;
      _selectedDate = date;
    });
    await _load(() => _client.byDate(date));
  }

  /// 重試當前正在看的目標(今天或某個歷史日期)。
  Future<void> _retry() {
    final date = _selectedDate;
    return date == null ? _loadToday() : _loadDate(date);
  }

  Future<void> _load(Future<Report> Function() fetch) async {
    try {
      final report = await fetch();
      if (!mounted) return;
      setState(() {
        _report = report;
        _state = _LoadState.data;
      });
    } on ReportApiException catch (e) {
      if (!mounted) return;
      setState(() {
        if (e.statusCode == 404) {
          _state = _LoadState.empty;
          _message = _selectedDate == null
              ? '今日報告尚未產生,稍後再回來看看。'
              : '這一天($_selectedDate)沒有報告。';
        } else {
          _state = _LoadState.error;
          _message = '讀取報告失敗(HTTP ${e.statusCode ?? '?'})';
        }
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _state = _LoadState.error;
        _message = '連線發生問題,請確認後端是否已啟動。';
      });
    }
  }

  /// 開歷史清單 bottom sheet:從 GET /reports 拿日期,選一天回看。
  Future<void> _openHistory() async {
    List<String> dates;
    try {
      dates = await _client.list();
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('讀取歷史清單失敗,請稍後再試。')),
      );
      return;
    }
    if (!mounted) return;

    final picked = await showModalBottomSheet<String>(
      context: context,
      showDragHandle: true,
      builder: (sheetContext) {
        if (dates.isEmpty) {
          return const Padding(
            padding: EdgeInsets.all(32),
            child: Center(child: Text('目前沒有歷史報告。')),
          );
        }
        return ListView.builder(
          shrinkWrap: true,
          itemCount: dates.length,
          itemBuilder: (context, index) {
            final date = dates[index];
            final isCurrent = date == _selectedDate;
            return ListTile(
              leading: const Icon(Icons.article_outlined),
              title: Text(date),
              trailing: isCurrent ? const Icon(Icons.check) : null,
              onTap: () => Navigator.of(sheetContext).pop(date),
            );
          },
        );
      },
    );

    if (picked != null) {
      await _loadDate(picked);
    }
  }

  @override
  Widget build(BuildContext context) {
    final viewingHistory = _selectedDate != null;
    return Scaffold(
      appBar: AppBar(
        title: const Text('arXiv 每日論文'),
        actions: [
          if (viewingHistory)
            IconButton(
              tooltip: '回到今天',
              icon: const Icon(Icons.today_outlined),
              onPressed: _loadToday,
            ),
          IconButton(
            tooltip: '歷史報告',
            icon: const Icon(Icons.history),
            onPressed: _openHistory,
          ),
        ],
      ),
      body: SafeArea(child: _buildBody()),
    );
  }

  Widget _buildBody() {
    switch (_state) {
      case _LoadState.loading:
        return const Center(child: CircularProgressIndicator());
      case _LoadState.empty:
        return _MessageView(
          icon: Icons.hourglass_empty,
          message: _message,
          actionLabel: '重新整理',
          onAction: _retry,
        );
      case _LoadState.error:
        return _MessageView(
          icon: Icons.cloud_off,
          message: _message,
          actionLabel: '重試',
          onAction: _retry,
        );
      case _LoadState.data:
        return ReportContent(report: _report!, onRefresh: _retry);
    }
  }
}

/// 空狀態 / 錯誤狀態共用的置中訊息 + 動作按鈕。
class _MessageView extends StatelessWidget {
  final IconData icon;
  final String message;
  final String actionLabel;
  final Future<void> Function() onAction;

  const _MessageView({
    required this.icon,
    required this.message,
    required this.actionLabel,
    required this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 48, color: theme.colorScheme.outline),
            const SizedBox(height: 16),
            Text(
              message,
              textAlign: TextAlign.center,
              style: theme.textTheme.bodyLarge,
            ),
            const SizedBox(height: 20),
            FilledButton.tonalIcon(
              onPressed: onAction,
              icon: const Icon(Icons.refresh),
              label: Text(actionLabel),
            ),
          ],
        ),
      ),
    );
  }
}
