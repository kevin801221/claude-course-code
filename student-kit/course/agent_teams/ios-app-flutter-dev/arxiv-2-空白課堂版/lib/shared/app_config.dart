/// App 全域設定 —— team lead 凍結的共用層地基。
///
/// 三個模組(reader / breathing / 後端對接)共用的常數都集中在這裡。
/// 數值來自 `_Context/app-spec.md` 的「研究結論」(已凍結)。
/// 要改任何一條，請走 mailbox 問 team lead、等批准，不要自己改。
library;

class AppConfig {
  const AppConfig._();

  /// 後端 FastAPI base URL。
  ///
  /// - iOS 模擬器 / macOS / 桌面：`http://127.0.0.1:8000`
  /// - Android 模擬器要改成 `http://10.0.2.2:8000`(模擬器用此 IP 連宿主機)
  ///
  /// 可在 build/run 時用 `--dart-define=BACKEND_BASE_URL=...` 覆寫。
  static const String backendBaseUrl = String.fromEnvironment(
    'BACKEND_BASE_URL',
    defaultValue: 'http://127.0.0.1:8000',
  );

  // ---- 閱讀提醒(breathing-owner 讀這裡，不要自己定 magic number)----

  /// 閱讀累積多久觸發呼吸提醒。
  ///
  /// 凍結預設 20 分鐘(對齊 20-20-20 法則，比 10 分鐘更有文獻依據；
  /// 見 research-findings.md)。可調 10 / 20 / 30 分鐘。
  static const Duration readingReminderThreshold = Duration(minutes: 20);

  /// demo / 現場展示用的短門檻 —— 讓 `flutter run` 不用等 20 分鐘就能看到呼吸動畫。
  ///
  /// 用 `--dart-define=DEMO=true` 啟用(見 [useDemoThreshold])。
  static const Duration readingReminderDemoThreshold = Duration(seconds: 20);

  /// 是否使用 demo 短門檻。run 時下 `--dart-define=DEMO=true` 開啟。
  static const bool useDemoThreshold =
      bool.fromEnvironment('DEMO', defaultValue: false);

  /// 實際生效的閱讀提醒門檻(demo 模式回短門檻，否則回正式門檻)。
  static Duration get effectiveReadingThreshold =>
      useDemoThreshold ? readingReminderDemoThreshold : readingReminderThreshold;

  // ---- 呼吸動畫(breathing-owner 讀這裡)----
  // Box Breathing 4-4-4-4：吸 4 → 屏 4 → 呼 4 → 屏 4，一輪 16 秒，做 3 輪 ≈ 48 秒，
  // 湊滿 60 秒 session(剩餘給引導文字)。依據見 research-findings.md。

  /// 呼吸動畫整段 session 時長。
  static const Duration breathingDuration = Duration(seconds: 60);

  /// Box Breathing 每一相(吸/屏/呼/屏)的秒數。
  static const Duration breathingPhaseDuration = Duration(seconds: 4);

  /// 一次呼吸 session 做幾輪。
  static const int breathingRounds = 3;
}
