var images = [];
var imageMap = new Map();

async function run() {
  let recvImages = await eel.get_images()();

  images = recvImages;

  images.forEach((element) => {
    createImageElement(element);
  });
}

function createImageElement(img_obj) {
  var img_64 = img_obj[0];
  var img_name = img_obj[1];

  var img_element = document.createElement("IMG");
  var img_src = "data:image/jpeg;base64," + img_64;
  img_element.setAttribute("src", img_src);

  var img_name_element = document.createTextNode(img_name);

  var new_img_cover = document.createElement("div");
  new_img_cover.classList.add("img_box");
  new_img_cover.appendChild(img_element);
  new_img_cover.appendChild(img_name_element);
  new_img_cover.onclick = function () {
    onClickImageCover(img_name);
  };

  document.getElementById("img_grid").appendChild(new_img_cover);
}

function createBookImageElement(img_obj) {
  var img_64 = img_obj[0];
  var img_name = img_obj[1];

  var img_element = document.createElement("IMG");
  var img_src = "data:image/jpeg;base64," + img_64;
  img_element.setAttribute("src", img_src);
  img_element.classList.add("img_book_cover");

  var new_img_cover = document.createElement("div");
  new_img_cover.classList.add("img_box");
  new_img_cover.appendChild(img_element);
  new_img_cover.onclick = function () {
    onClickBookImage(img_name);
  };

  document.getElementById("img_grid").appendChild(new_img_cover);
}

function onClickImageCover(img_name) {
  sessionStorage.setItem("currentBook", img_name);
  console.log("Saving ${img_name} in storage");
  window.location.href = "http://localhost:8000/book.html";
}

async function run_book() {
  var currentPage = sessionStorage.getItem("currentBook");

  let recvImages = await eel.get_folder_images(currentPage)();
  images = recvImages;

  images.forEach((element) => {
    createBookImageElement(element);
    imageMap.set(element[1], element[0]);
  });
}

function onClickBookImage(img_name) {
  sessionStorage.setItem("currentPage", img_name);
  console.log("Saving ${img_name} in storage");

  var image = imageMap.get(img_name);

  var overlay = document.getElementById("overlay");
  overlay.style.display = "grid";

  overlay.onclick = function () {
    onClickOverlayOff();
  };

  var imgBox = document.getElementById("image_overlay");

  var img_element = document.createElement("IMG");
  var img_src = "data:image/jpeg;base64," + image;
  img_element.setAttribute("src", img_src);
  img_element.classList.add("img_overlay");

  var arrowRight = document.createElement("i");
  arrowRight.classList.add("arrow");
  arrowRight.classList.add("right");

  var arrowrLeft = document.createElement("i");
  arrowrLeft.classList.add("arrow");
  arrowrLeft.classList.add("left");

  imgBox.appendChild(arrowrLeft);
  imgBox.appendChild(img_element);
  imgBox.appendChild(arrowRight);

  // imgBox.onkeypress = onArrowPress(event, imgBox, imageName);

  imgBox.addEventListener("keypress", function (event) {
    if (event.key === "ArrowLeft") {
      imgBox.childNodes[0].setAttribute(
        "src",
        "data:image/jpeg;base64," +
          imageMap.get(parseImageName(img_name, "left", imageMap.size()))
      );
    }
    if (event.key === "ArrowRight") {
      imgBox.childNodes[0].setAttribute(
        "src",
        "data:image/jpeg;base64," +
          imageMap.get(parseImageName(img_name, "right", imageMap.size()))
      );
    }
  });
}

function onArrowPress(event, imgBox, imageName) {
  if (event.key === "ArrowLeft") {
    imgBox.childNodes[0].setAttribute(
      "src",
      "data:image/jpeg;base64," +
        imageMap.get(parseImageName(imageName, "left", imageMap.size()))
    );
  }
  if (event.key === "ArrowRight") {
    imgBox.childNodes[0].setAttribute(
      "src",
      "data:image/jpeg;base64," +
        imageMap.get(parseImageName(imageName, "right", imageMap.size()))
    );
  }
}

function onClickOverlayOff() {
  document.getElementById("overlay").style.display = "none";
  var imgBox = document.getElementById("image_overlay");
  imgBox.childNodes.forEach((item) => {
    imgBox.removeChild(item);
  });
}

function parseImageName(imageName, direction, imagesLen) {
  var imgNumber = imageName.substring(imageName.indexOf("."), 0);
  var imgType = imageName.substring(imageName.indexOf("."));

  if (direction == "left" && imgNumber < imagesLen) {
    imgNumber += 1;
  } else if (direction == "right" && imgNumber > 1) {
    imgNumber -= 1;
  }

  return imgNumber + imgType;
}
