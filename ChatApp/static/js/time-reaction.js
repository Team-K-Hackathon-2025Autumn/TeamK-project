// クラスによりdocument内のすべてのリアクション数を取得
const reactionCounts = document.querySelectorAll('.reaction-counts');

// reactionCountsを一つずつelementとして処理
reactionCounts.forEach((element) => {
  // elementの数を数値に10進数の数値に変換
  const eachCount = parseInt(element.textContent, 10);
  // そのカウントが書かれているボタンをelementの親要素のbuttonとして取得
  const reactionMsgBtn = element.closest('button');
  // reactionMsgBtn.style.transition = '0.3s ease';
  // eachCountの値によってスタイルを変更
  if (eachCount === 0) {
    reactionMsgBtn.style.fontSize = '0.6rem';
    reactionMsgBtn.style.opacity = '0.3';
  } else if (eachCount < 5) {
    reactionMsgBtn.style.fontSize = '0.6rem';
    reactionMsgBtn.style.opacity = '1.0';
    // reactionMsgBtn.style.border = '1px #00c9ad solid';
    reactionMsgBtn.style.color = 'white';
    reactionMsgBtn.style.backgroundColor = '#a97777';
  } else if (eachCount < 10) {
    reactionMsgBtn.style.fontSize = '0.8rem';
    reactionMsgBtn.style.opacity = '1.0';
    // reactionMsgBtn.style.border = '1px #00c9ad solid';
    reactionMsgBtn.style.color = 'white';
    reactionMsgBtn.style.backgroundColor = '#a97777';
  } else if (eachCount < 20) {
    reactionMsgBtn.style.fontSize = '1.0rem';
    reactionMsgBtn.style.opacity = '1.0';
    reactionMsgBtn.style.color = 'white';
    reactionMsgBtn.style.backgroundColor = '#a97777';
    // reactionMsgBtn.style.border = '2px #00c9ad solid';
  } else if (eachCount < 100) {
    reactionMsgBtn.style.fontSize = '1.2rem';
    reactionMsgBtn.style.opacity = '1.0';
    reactionMsgBtn.style.color = 'white';
    reactionMsgBtn.style.backgroundColor = '#a97777';
    // reactionMsgBtn.style.border = '2px #00c9ad solid';
  } else {
    reactionMsgBtn.style.fontSize = '1.4rem';
    reactionMsgBtn.style.opacity = '1.0';
    reactionMsgBtn.style.color = 'white';
    reactionMsgBtn.style.backgroundColor = '#a97777';
    // reactionMsgBtn.style.border = '2px #00c9ad solid';
  }
});

// 画面に表示されたdatetimeを取得(他の人のコメント)
const otherDateTimes = document.querySelectorAll('.other-sendTime');

// dateTimesを一つずつ処理
otherDateTimes.forEach((element2) => {
  const eachDateTime = element2.textContent;

  // eachDateTimeをスペースの部分で分ける
  const splitedDate = eachDateTime.split(' '),
    // 分けた前半をymd、後半をhmsとして取得
    ymd = splitedDate[0],
    hms = splitedDate[1];

  // さらにymdをハイフンの部分で分ける
  const date = ymd.split('-'),
    year = date[0],
    month = date[1],
    day = date[2];

  // さらにhmsをコロンの部分で分ける
  const time = hms.split(':'),
    hour = time[0],
    minute = time[1],
    second = time[2];

  // element2に月日（改行）時分をセットする
  element2.innerHTML = `${year}/${month}/${day}<br>${hour}:${minute}`;
});

// 画面に表示されたdatetimeを取得(自分のコメント)
const myDateTimes = document.querySelectorAll('.my-sendTime');

// dateTimesを一つずつ処理
myDateTimes.forEach((element2) => {
  const eachDateTime = element2.textContent;

  // eachDateTimeをスペースの部分で分ける
  const splitedDate = eachDateTime.split(' '),
    // 分けた前半をymd、後半をhmsとして取得
    ymd = splitedDate[0],
    hms = splitedDate[1];

  // さらにymdをハイフンの部分で分ける
  const date = ymd.split('-'),
    year = date[0],
    month = date[1],
    day = date[2];

  // さらにhmsをコロンの部分で分ける
  const time = hms.split(':'),
    hour = time[0],
    minute = time[1],
    second = time[2];

  // element2に月日（改行）時分をセットする
  element2.innerHTML = `${year}/${month}/${day}<br>${hour}:${minute}`;
});
