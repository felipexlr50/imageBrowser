var images = [];
var imageMap = new Map();

async function run() {
  images = recvImages;

  images.forEach((element) => {
    createImageElement(element);
  });
}

function createImageElement(img_obj) {
  var img_64 = img_obj["img"];
  var img_name = img_obj["name"];

  var img_element = document.createElement("IMG");
  var img_src = "data:image/jpeg;base64," + img_64;
  img_element.setAttribute("src", img_src);

  var img_name_element = document.createTextNode(img_name);

  var new_img_cover = document.createElement("div");
  new_img_cover.classList.add("img_box");
  new_img_cover.appendChild(img_element);
  new_img_cover.appendChild(img_name_element);
  new_img_cover.onclick = function () {
    onClickImageCover(img_obj);
  };

  document.getElementById("img_grid").appendChild(new_img_cover);
}

function onClickImageCover(img_obj) {
  sessionStorage.setItem("currentBook", JSON.stringify(img_obj));
  window.location.href = "/book/" + img_obj["id"];
}

document.getElementById("search_btn").onclick = function () {
  var inputQuery = document.getElementById("search_bar").value;
  window.location.href = "/search/" + inputQuery;
};
