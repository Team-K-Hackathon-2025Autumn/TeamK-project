/*
リアクションボタンを押した場合、スクロール位置をセッションストレージに保存。
メッセージ一覧読み込み時に、セッションストレージに値があるかチェックし、存在した場合スクロール位置を使用して復元、復元後にセッションストレージを削除。
値がない場合、最下部へスクロールした状態で表示
*/

const element = document.getElementById('message-area');
const deleteButton = document.getElementById('button');
const path = window.location.pathname;
const savedscrollTopPosition = sessionStorage.getItem('scrollY_' + path);
if (savedscrollTopPosition) {
  element.scrollTop = parseInt(savedscrollTopPosition, 10);
} else {
  element.scrollTo(0, element.scrollHeight);
}

sessionStorage.removeItem('scrollY_' + path);

const reactionButtons = document.querySelectorAll('.reaction-message-button');

reactionButtons.forEach((button) => {
  button.addEventListener('click', function (event) {
    console.log('a');
    const path = window.location.pathname;
    const scrollTopPosition = element.scrollTop;
    sessionStorage.setItem('scrollY_' + path, scrollTopPosition);
  });
});
