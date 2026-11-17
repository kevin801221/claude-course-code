import 'dart:convert';

import 'package:http/http.dart' as http;

import 'app_config.dart';
import 'models.dart';

/// 呼叫後端報告 API 的唯一介面(team lead 凍結的共用層)。
///
/// 前端隊友(reader-owner)只透過這個 client 拿資料,**不直接碰 HTTP / 後端細節**。
/// 對應契約:
///   GET /reports/today   → Report
///   GET /reports         → `List<String>`(歷史報告日期,新到舊)
///   GET /reports/{date}  → Report
class ReportApiClient {
  final http.Client _http;
  final String baseUrl;

  ReportApiClient({http.Client? httpClient, String? baseUrl})
      : _http = httpClient ?? http.Client(),
        baseUrl = baseUrl ?? AppConfig.backendBaseUrl;

  /// 今天的報告。
  Future<Report> today() async {
    final json = await _getJson('/reports/today');
    return Report.fromJson(json as Map<String, dynamic>);
  }

  /// 歷史報告日期清單(新到舊)。
  Future<List<String>> list() async {
    final json = await _getJson('/reports');
    if (json is List) {
      return json.map((e) => e.toString()).toList();
    }
    // 容錯:後端若包成 { dates: [...] }
    if (json is Map && json['dates'] is List) {
      return (json['dates'] as List).map((e) => e.toString()).toList();
    }
    return const [];
  }

  /// 指定日期的報告。
  Future<Report> byDate(String date) async {
    final json = await _getJson('/reports/$date');
    return Report.fromJson(json as Map<String, dynamic>);
  }

  Future<dynamic> _getJson(String path) async {
    final uri = Uri.parse('$baseUrl$path');
    final resp = await _http.get(uri, headers: {'Accept': 'application/json'});
    if (resp.statusCode != 200) {
      throw ReportApiException(
        'GET $path 失敗 (HTTP ${resp.statusCode})',
        statusCode: resp.statusCode,
      );
    }
    return jsonDecode(utf8.decode(resp.bodyBytes));
  }

  void dispose() => _http.close();
}

/// 後端呼叫失敗時拋出。reader-owner 用它顯示錯誤狀態。
class ReportApiException implements Exception {
  final String message;
  final int? statusCode;
  ReportApiException(this.message, {this.statusCode});

  @override
  String toString() => 'ReportApiException: $message';
}
