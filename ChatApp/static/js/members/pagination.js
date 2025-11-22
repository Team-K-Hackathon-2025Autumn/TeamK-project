/*
メンバー一覧ページでレスポンスが返ってきた後、
メンバー一覧の配列データをもとにページネーションの作成・制御をする
*/

/*
ページネーションを作成・制御する関数。
*/
const pagination = () => {
  try {
    let page = 1; // 今何ページ目にいるか
    const STEP = 5; // ステップ数（1ページに表示する項目数）

    // 全ページ数を計算
    // 「メンバーの総数/(割る)ステップ数」の余りの有無で場合分け
    // 余りがある場合は１ページ余分に追加する
    const TOTAL =
      members.length % STEP == 0
        ? members.length / STEP
        : Math.floor(members.length / STEP) + 1;

    // ページネーションで表示されるページ数部分（< 1 / 2 >）の要素を作成
    const updatePageDisplay = (currentPage, totalPages) => {
      const paginationUl = document.querySelector('.pagination');
      // 中身をリセット
      paginationUl.innerHTML = '';

      const li = document.createElement('li');
      li.innerText = `${currentPage} / ${totalPages}`;
      li.style.pointerEvents = 'none';
      paginationUl.appendChild(li);
    };

    // メンバー名の要素を作成
    const createMembersList = (page, STEP) => {
      const ul = document.querySelector('.member-box');
      // 一度メンバーリストを空にする
      ul.innerHTML = '';

      const firstMemberInPage = (page - 1) * STEP + 1;
      const lastMemberInPage = page * STEP;

      // 各メンバー要素の作成
      members.forEach((member, i) => {
        if (i < firstMemberInPage - 1 || i > lastMemberInPage - 1) return;
        const a = document.createElement('a');
        const li = document.createElement('li');
        a.innerText = member.name;
        li.appendChild(a);
        ul.appendChild(li);
      });
    };

    const init = (page, STEP) => {
      createMembersList(page, STEP);
      updatePageDisplay(page, TOTAL);
    };

    // 初期動作時に1ページ目を表示
    init(page, STEP);

    // 前ページ遷移
    document.getElementById('prev').addEventListener('click', () => {
      if (page <= 1) return;
      page = page - 1;
      init(page, STEP);
    });

    // 次ページ遷移
    document.getElementById('next').addEventListener('click', () => {
      if (page >= members.length / STEP) return;
      page = page + 1;
      init(page, STEP);
    });

    return true;
  } catch (error) {
    console.log(`エラー：${error}`);
    return false;
  }
};

pagination();
// DOMツリーが構築されたらpagination関数を発火（ページネーションを作成し、その後チャンネル追加ボタンを作成・表示）
document.addEventListener('DOMContentLoaded', function () {
  try {
    pagination();
  } catch (error) {
    console.log(`エラー：${error}`);
  }
});
