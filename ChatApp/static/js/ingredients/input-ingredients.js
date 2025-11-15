// 食材入力フォームを表示するモーダルの制御
isModalCloseDisabled = false;
const inputButton = document.getElementById('create-menu');
// おそらく()内をmessage.htmlのボタン名と合わせる
const inputIngredientsModal = document.getElementById(
  'input-ingredients-modal'
);
//おそらく()内をmodal/input-ingredients.htmlのidと合わせる
const inputPageButtonClose = document.getElementById('input-page-close-button');
// おそらく()内を×ボタンのidと合わせる

// モーダル表示ボタンが押された時にモーダルを表示する
inputButton.addEventListener('click', () => {
  inputIngredientsModal.style.display = 'flex';
});

// モーダル内のXボタンが押された時にモーダルを非表示にする
inputPageButtonClose.addEventListener('click', () => {
  if (!isModalCloseDisabled) {
    inputIngredientsModal.style.display = 'none';
  }
});

// 画面のどこかが押された時にモーダルを非表示にする
addEventListener('click', (e) => {
  if (!isModalCloseDisabled) {
    if (e.target == inputIngredientsModal) {
      inputIngredientsModal.style.display = 'none';
    }
  }
});

// -----ここから食材入力エリアの制御-----
// ロードした時に入力エリアを１つ加える
window.onload = function () {
  add_input_area();
};

// .input-areaを１つ加える関数
function add_input_area() {
  var inputarea = document.querySelector('#add-input-area');
  var num = 0;
  if (inputarea !== null) {
    num = inputarea.childElementCount;
  }
  num++;

  var ingre = create_ingre_input(num);
  var quant = create_quant_input(num);
  var unit = create_unit_input(num);
  var del_btn = create_delete_button(num);

  var input_area = document.createElement('div');
  input_area.setAttribute('id', 'input-area-' + num);
  input_area.setAttribute('class', 'input-area');
  input_area.appendChild(ingre);
  input_area.appendChild(quant);
  input_area.appendChild(unit);
  input_area.appendChild(del_btn);

  var input = document.getElementById('add-input-area');
  input.appendChild(input_area);

  set_delete_btn_disabled();

  set_add_btn_disabled();
}

// .input-areaを１つ削除する関数
function delete_form_element(name) {
  var elem = document.getElementById(name);
  elem.remove();

  var inputs = document.getElementById('add-input-area').children;

  for (i = 0; i < inputs.length; i++) {
    // インプット欄のID番号の付け直し
    inputs[i].id = 'input-area-' + (i + 1);
    // 食材入力欄、数量、単位のID番号の付け直し
    inputs[i].children[0].id = 'input-ingre-' + (i + 1);
    inputs[i].children[1].id = 'input-quant-' + (i + 1);
    inputs[i].children[2].id = 'input-unit-' + (i + 1);
    // 削除ボタンの作り直し
    inputs[i].children[3].remove();
    var btn = create_delete_button(i + 1);
    inputs[i].appendChild(btn);
  }

  set_delete_btn_disabled();

  set_add_btn_disabled();
}

// 食材入力欄
function create_ingre_input(num) {
  var input_ingre = document.createElement('input');
  input_ingre.setAttribute('class', 'ingre');
  input_ingre.setAttribute('id', 'input-ingre-' + num);
  input_ingre.setAttribute('name', 'name');
  input_ingre.setAttribute('placeholder', '食材名');
  input_ingre.setAttribute('required', '');
  return input_ingre;
}

// 数量入力欄
function create_quant_input(num) {
  var input_quant = document.createElement('input');
  input_quant.setAttribute('class', 'quant');
  input_quant.setAttribute('id', 'input-quant-' + num);
  input_quant.setAttribute('name', 'quantity');
  input_quant.setAttribute('placeholder', '数量');
  input_quant.setAttribute('required', '');
  return input_quant;
}

// 単位入力欄
function create_unit_input(num) {
  var option_1 = document.createElement('option');
  var option_1_txt = document.createTextNode(' ');
  option_1.setAttribute('value', '""');
  option_1.appendChild(option_1_txt);

  var option_2 = document.createElement('option');
  var option_2_txt = document.createTextNode('個');
  option_2.setAttribute('value', '個');
  option_2.appendChild(option_2_txt);

  var option_3 = document.createElement('option');
  var option_3_txt = document.createTextNode('g');
  option_3.setAttribute('value', 'g');
  option_3.appendChild(option_3_txt);

  var option_4 = document.createElement('option');
  var option_4_txt = document.createTextNode('ml');
  option_4.setAttribute('value', 'ml');
  option_4.appendChild(option_4_txt);

  var input_unit = document.createElement('select');
  input_unit.setAttribute('class', 'unit');
  input_unit.setAttribute('id', 'input-unit-' + num);
  input_unit.setAttribute('name', 'unit');
  input_unit.setAttribute('required', '');
  input_unit.appendChild(option_1);
  input_unit.appendChild(option_2);
  input_unit.appendChild(option_3);
  input_unit.appendChild(option_4);
  return input_unit;
}

// 削除ボタン
function create_delete_button(num) {
  var btn = document.createElement('button');
  var btn_txt = document.createTextNode('×');
  btn.appendChild(btn_txt);
  btn.setAttribute('class', 'del_btn');
  btn.setAttribute('type', 'button');
  btn.setAttribute('onclick', 'delete_form_element("input-area-' + num + '");');
  return btn;
}

// 削除ボタンの有効無効の設定
function set_delete_btn_disabled() {
  var form = document.getElementById('add-input-area');
  var buttons = form.getElementsByTagName('button');
  if (buttons.length == 1) {
    buttons[0].disabled = true;
  } else {
    for (i = 0; i < buttons.length; i++) {
      buttons[i].disabled = false;
    }
  }
}

// 追加ボタンの有効無効の設定
function set_add_btn_disabled() {
  var form = document.getElementById('add-input-area');
  var buttons = form.getElementsByTagName('button');
  if (buttons.length < 9) {
    document.getElementsByClassName('add-btn')[0].disabled = false;
  } else {
    document.getElementsByClassName('add-btn')[0].disabled = true;
  }
}
