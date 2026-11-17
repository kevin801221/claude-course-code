/// 後端報告 API 的唯一前端介面 —— team lead 凍結的共用層。
///
/// reader-owner / breathing-owner **只透過這個 client 拿資料**，
/// 不要自己寫 http / jsonDecode，也不要假設後端細節。
/// 要改介面簽章，先用 mailbox 問 team lead、等批准。
library;

import 'dart:convert';

import 'package:http/http.dart' as http;

import 'app_config.dart';
import 'models.dart';

/// 呼叫後端報告 API 時的錯誤。`statusCode` 為 HTTP 狀態碼(無回應時為 null)。
class ReportApiException implements Exception {
  final String message;
  final int? statusCode;

  const ReportApiException(this.message, {this.statusCode});

  @override
  String toString() =>
      'ReportApiException($statusCode): $message';
}

/// 對接後端三個契約端點的 client。
class ReportApiClient {
  final http.Client _client;
  final String baseUrl;

  ReportApiClient({http.Client? client, String? baseUrl})
      : _client = client ?? http.Client(),
        baseUrl = baseUrl ?? AppConfig.backendBaseUrl;

  /// `GET /reports/today` → 今日報告。
  Future<Report> today() async {
    final json = await _getJson('/reports/today');
    return Report.fromJson(json as Map<String, dynamic>);
  }

  /// `GET /reports` → 歷史報告日期清單(新到舊)。
  Future<List<String>> list() async {
    final json = await _getJson('/reports');
    if (json is List) {
      return json.map((e) => e.toString()).toList();
    }
    throw const ReportApiException('GET /reports 回傳格式非清單');
  }

  /// `GET /reports/{date}` → 指定日期報告。
  Future<Report> byDate(String date) async {
    final json = await _getJson('/reports/$date');
    return Report.fromJson(json as Map<String, dynamic>);
  }

  Future<dynamic> _getJson(String path) async {
    final uri = Uri.parse('$baseUrl$path');
    late http.Response res;
    try {
      res = await _client.get(uri, headers: {'Accept': 'application/json'});
    } catch (e) {
      throw ReportApiException('連不上後端：$e');
    }
    if (res.statusCode != 200) {
      throw ReportApiException(
        '後端回應 ${res.statusCode}',
        statusCode: res.statusCode,
      );
    }
    try {
      return jsonDecode(utf8.decode(res.bodyBytes));
    } catch (e) {
      throw ReportApiException('回應 JSON 解析失敗：$e',
          statusCode: res.statusCode);
    }
  }

  void close() => _client.close();
}
