/*
グループ一覧ページでレスポンスが返ってきた後、
グループ一覧の配列データをもとにスクロール形式で表示する
*/

import { initCreategroupModal } from '/static/js/groups/create-group.js';
import { initDeletegroupModal } from '/static/js/groups/delete-group.js';

const deletegroupModal = document.getElementById('delete-group-modal');

const groupBox = document.querySelector('.group-box'); // グループリストを表示するコンテナ

const STEP = 5; // 一度に表示するグループ数
let displayedCount = 0; // 現在表示しているグループ数

// グループを追加表示する関数
const appendGroups = () => {
  const nextGroups = groups.slice(displayedCount, displayedCount + STEP);

  nextGroups.forEach((group) => {
    const wrapper = document.createElement('div');
    wrapper.classList.add('group-item-wrapper');

    const li = document.createElement('li');
    li.classList.add('group-item');

    let ownershipType = '';
    if (uid === group.created_by) {
      ownershipType = 'オーナー';
    } else {
      ownershipType = 'メンバー';
    }

    li.style.backgroundColor = 'white'; // 好きな色を指定
    li.style.color = '#5D4037';
    li.textalign = 'center';
    li.style.width = '295px';
    li.style.height = '40px';
    const ownwership = document.createElement('div');
    ownwership.innerHTML = ownershipType;
    ownwership.classList.add('ownershipType');
    li.appendChild(ownwership);

    const a = document.createElement('a');
    a.innerText = group.name;
    a.setAttribute('href', `/group/${group.id}`);
    li.appendChild(a);

    wrapper.appendChild(li);

    li.style.backgroundColor = '#ffffffff'; // 好きな色を指定
    li.style.color = '#5D4037';
    li.style.width = '100%';
    li.style.height = '40px';
    li.style.padding = '12px';
    li.style.borderRadius = '10px';
    li.style.marginBottom = '8px';
    li.style.boxShadow = '0px 2px 4px rgba(0, 0, 0, 0.08)';
    li.style.display = 'flex';
    li.style.justifyContent = 'space-between';
    li.style.alignItems = 'center';

    // 作成者のみ削除ボタンを表示
    if (uid === group.created_by) {
      const deleteButton = document.createElement('button');
      deleteButton.innerHTML = '<ion-icon name="trash-outline"></ion-icon>';
      deleteButton.classList.add('delete-button');
      li.appendChild(deleteButton);

      deleteButton.addEventListener('click', () => {
        deletegroupModal.style.display = 'flex';
        const deleteGroupForm = document.getElementById('deletegroupForm');
        deleteGroupForm.action = `/group/${group.id}/delete`;
      });
    }

    groupBox.appendChild(wrapper);
  });

  displayedCount += nextGroups.length;
};

// 初期表示（最初の5件）
appendGroups();

// スクロールで追加表示
groupBox.addEventListener('scroll', () => {
  if (
    groupBox.scrollTop + groupBox.clientHeight >=
    groupBox.scrollHeight - 40
  ) {
    if (displayedCount < groups.length) {
      appendGroups();
    }
  }
});

// 削除モーダル初期化
initDeletegroupModal();
initCreategroupModal();
