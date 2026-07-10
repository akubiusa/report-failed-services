# GitHub Copilot コードレビュー指示

`report-failed-services` は systemctl で Failed となったサービスを検知し Discord に通知する Python ツールです。レビュー時は以下を基準にしてください。

## 強制されている規約

- **Lint**: CI は `flake8 . --count --select=E1,E2,E3,E4,E7,E9,W1,W2,W3,W4,W5,F63,F7,F82 --show-source --statistics` を実行する。この select 範囲のエラーが残る変更は指摘する。
- **コミット/PR**: Conventional Commits (`<type>(<scope>): <description>`)。description は日本語。
- **表記**: 日本語と英数字の間に半角スペースを入れる。
- **docstring**: 関数・クラスには日本語で docstring を記述する。

## 重点的に確認する点

- **機密情報**: `DISCORD_TOKEN` などの認証情報がハードコード・コミットされていないか。ログにトークンやチャンネル ID を出力していないか。
- **エラーハンドリング**: `systemctl` の実行結果や Discord API 呼び出し (`requests`) の失敗を握りつぶしていないか。
- **状態管理**: `notified_ids.json` の読み書きで通知の重複・欠落を招く変更がないか。

## 誤検知しやすい既知パターン (フラグ不要)

- **自動テストの不在**: `tests/` は存在しない。テストファイルの追加を一律に要求しない (動作確認は実機/手動)。
- **`subprocess` + `shell=True`**: `systemctl` 呼び出しは固定文字列であり意図的。ユーザー入力を渡していない限りインジェクションとして指摘しない。
- **Linux/Systemd 前提**: クロスプラットフォーム対応の欠如は指摘しない。本ツールは Systemd 稼働の Linux 環境専用。
