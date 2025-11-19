/* リアクションのカウント数により背景色等を変える
1. 各メッセージのリアクションカウント数を取得
2. 各メッセージのリアクションカウント数により処理を分ける */

// クラスによりdocument内のすべてのリアクション数を取得
const reactionCounts = document.querySelectorAll('.reaction-counts');

// reactionCountsを一つずつelementとして処理
reactionCounts.forEach(element => {
    // elementの数を数値に10進数の数値に変換
    const eachCount = parseInt(element.textContent,10);
    // そのカウントが書かれているボタンをelementの親要素のbuttonとして取得
    const reactionMsgBtn = element.closest('button');

    // eachCountの値によってスタイルを変更
    if (eachCount === 0) {
    reactionMsgBtn.style.fontSize = '0.6rem';
    reactionMsgBtn.style.opacity = '0.3';
} else if (eachCount < 5) {
    reactionMsgBtn.style.fontSize = '0.8rem';
    reactionMsgBtn.style.opacity = '1.0';
} else if (eachCount < 10) {
    reactionMsgBtn.style.fontSize = '1.0rem';
    reactionMsgBtn.style.opacity = '1.0';
} else if (eachCount < 20) {
    reactionMsgBtn.style.fontSize = '1.0rem';
    reactionMsgBtn.style.opacity = '1.0';
    reactionMsgBtn.style.color = 'rgba(253, 126, 0, 1.0)'; 
    reactionMsgBtn.style.fontWeight = 'bold'
} else if (eachCount < 100) {
    reactionMsgBtn.style.fontSize = '1.0rem';
    reactionMsgBtn.style.opacity = '1.0';
    reactionMsgBtn.style.backgroundColor = 'rgba(253, 126, 0, 1.0)';
    reactionMsgBtn.style.color = 'white';  
} else {
    reactionMsgBtn.style.fontSize = '1.2rem';
    reactionMsgBtn.style.opacity = '1.0';
    reactionMsgBtn.style.backgroundColor = 'rgba(253, 126, 0, 1.0)';     
    reactionMsgBtn.style.color = 'white'; 
}
});