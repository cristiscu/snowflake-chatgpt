-- (obsolete --> not functional, don't try it!)

CREATE API INTEGRATION openai_ai
   API_PROVIDER = 'AWS_API_GATEWAY'
   API_AWS_ROLE_ARN = 'arn:aws:iam::478284724651:role/openAIAPIGatewayRole'
   API_ALLOWED_PREFIXES = ('https://n1ut983r9l.execute-api.us-east-2.amazonaws.com/main/openai/v1/completions')
   ENABLED = true;
DESCRIBE INTEGRATION openai_ai;

CREATE OR REPLACE FUNCTION openai_req("EVENT" OBJECT)
   RETURNS OBJECT
   LANGUAGE JAVASCRIPT
AS '
return {"body": {
"model": "text-davinci-003",
"prompt": EVENT.body.data[0][1],
"temperature": 0,
"max_tokens": 100,
"top_p": 1,
"frequency_penalty": 0.0,
"presence_penalty": 0.0
}
};';

CREATE OR REPLACE FUNCTION openai_resp("EVENT" OBJECT)
   RETURNS OBJECT
   LANGUAGE JAVASCRIPT
AS '
let array_of_rows_to_return = [[0, EVENT.body]];
return {"body": {"data": array_of_rows_to_return}};
';

CREATE OR REPLACE EXTERNAL FUNCTION openai_ext("QUESTION" VARCHAR(16777216))
   RETURNS VARIANT
   API_INTEGRATION = openai_ai
   MAX_BATCH_ROWS = 100
   REQUEST_TRANSLATOR = openai_req
   RESPONSE_TRANSLATOR = openai_resp
AS 'https://n1u9451r9l.execute-api.us-east-2.amazonaws.com/main/openai/v1/completions';

select openai_ext('Classify this sentiment: OpenAI is Awesome!')::VARIANT:choices[0]:text as response;
