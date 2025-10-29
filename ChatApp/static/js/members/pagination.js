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
    const STEP = 8; // ステップ数（1ページに表示する項目数）

    // 全ページ数を計算
    // 「メンバーの総数/(割る)ステップ数」の余りの有無で場合分け
    // 余りがある場合は１ページ余分に追加する
    const TOTAL =
      channels.length % STEP == 0
        ? channels.length / STEP
        : Math.floor(channels.length / STEP) + 1;

    // ページネーションで表示されるページ数部分（< 1 2 3 >）の要素を作成
    const paginationUl = document.querySelector(".pagination");
    let pageCount = 0;
    while (pageCount < TOTAL) {
      let pageNumber = document.createElement("li");
      pageNumber.dataset.pageNum = pageCount + 1;
      pageNumber.innerText = pageCount + 1;
      paginationUl.appendChild(pageNumber);
      // ページネーションの数字部分が押された時にもページが変わるように処理
      pageNumber.addEventListener("click", (e) => {
        const targetPageNum = e.target.dataset.pageNum;
        page = Number(targetPageNum);
        init(page, STEP);
      });
      pageCount++;
    }

    // メンバー名の要素を作成
    const createMembersList = (page, STEP) => {
      const ul = document.querySelector(".member-box");
      // 一度メンバーリストを空にする
      ul.innerHTML = "";

      const firstMemberInPage = (page - 1) * STEP + 1;
      const lastMemberInPage = page * STEP;

      // 各メンバー要素の作成
      members.forEach((member, i) => {
        if (i < firstMemberInPage - 1 || i > lastMemberInPage - 1) return;
        const a = document.createElement("a");
        const li = document.createElement("li");
        a.innerText = member.name;
        li.appendChild(a);
        ul.appendChild(li);
      });
    };

    // ページネーション内で現在選択されているページの番号に色を付ける
    const colorPaginationNum = () => {
      // ページネーションの数字部分の全要素から"colored"クラスを一旦取り除く
      const paginationArr = [...document.querySelectorAll(".pagination li")];
      paginationArr.forEach((page) => {
        page.classList.remove("colored");
      });
      // 選択されているページにclass="colored"を追加（文字色が変わる）
      paginationArr[page - 1].classList.add("colored");
    };

    const init = (page, STEP) => {
      createMembersList(page, STEP);
      colorPaginationNum();
    };
    // 初期動作時に1ページ目を表示
    init(page, STEP);

    // 前ページ遷移
    document.getElementById("prev").addEventListener("click", () => {
      if (page <= 1) return;
      page = page - 1;
      init(page, STEP);
    });

    // 次ページ遷移
    document.getElementById("next").addEventListener("click", () => {
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

// DOMツリーが構築されたらpagination関数を発火（ページネーションを作成し、その後チャンネル追加ボタンを作成・表示）
document.addEventListener("DOMContentLoaded", function () {
  try {
    pagination();
  } catch (error) {
    console.log(`エラー：${error}`);
  }
});
