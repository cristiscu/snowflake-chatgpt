# Run with: .\app.ps1

$prompt = "What is Snowflake Data Cloud"

Invoke-Expression ("curl -i -X POST" +
  " -H 'Content-Type: application/json'" +
  " -H 'Authorization: Bearer $env:OPENAI_API_KEY'" +
  " -d '{ `"model`": `"gpt-4-1106-preview`"," +
  " `"messages`": [{`"role`": `"user`", `"content`": `"$prompt`"}] }'" +
  " 'https://api.openai.com/v1/chat/completions'")
