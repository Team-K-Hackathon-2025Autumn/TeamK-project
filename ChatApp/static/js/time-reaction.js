/* リアクションのカウント数により背景色等を変える
1. 各メッセージのリアクションカウント数を取得
2. 各メッセージのリアクションカウント数により処理を分ける */

let reaction_counts = ${messages.count}
const reaction_msg_btn =document.getElementsByClassName('reaction-message-button');
if (reaction_counts === 0) {
    reaction_msg_btn.style.fontsize('0.6rem');
    reaction_msg_btn.style.opacity('0.3');
} else if (reaction_counts < 4) {
    reaction_msg_btn.style.fontsize('0.8rem');
    reaction_msg_btn.style.opacity('1.0');
} else if (reaction_counts < 10) {
    reaction_msg_btn.style.fontsize('1.0rem')
    reaction_msg_btn.style.opacity('1.0')
} else if (reaction_counts < 20) {
    reaction_msg_btn.style.fontsize('1.0rem')
    reaction_msg_btn.style.opacity('1.0')
} else if (reaction_counts <100) {

} else {

}