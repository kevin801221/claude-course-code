/// App 全域設定(team lead 凍結的共用層)。
///
/// 後端 base URL 從這裡讀。要改請走 mailbox 問 team lead。
class AppConfig {
  const AppConfig._();

  /// 後端 FastAPI base URL。
  ///
  /// - iOS 模擬器 / 桌面:`http://127.0.0.1:8000`
  /// - Android 模擬器要改成 `http://10.0.2.2:8000`(模擬器用此 IP 連宿主機)
  ///
  /// 可在 build/run 時用 `--dart-define=BACKEND_BASE_URL=...` 覆寫。
  static const String backendBaseUrl = String.fromEnvironment(
    'BACKEND_BASE_URL',
    defaultValue: 'http://127.0.0.1:8000',
  );

  /// 閱讀累積多久觸發呼吸提醒(研究結論凍結後填入,見 app-spec.md)。
  /// 預設 10 分鐘;確切依據由 researcher 收斂後 team lead 凍結。
  static const Duration readingReminderThreshold = Duration(minutes: 10);

  /// 呼吸動畫總時長。
  static const Duration breathingDuration = Duration(seconds: 60);
}
