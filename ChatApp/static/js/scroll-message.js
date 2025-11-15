/*
メッセージ一覧ページ内、ページ読み込み時に自動で下までスクロールする
*/

const element = document.getElementById('message-area');
element.scrollTo(0, element.scrollHeight);
