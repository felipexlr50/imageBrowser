var images = [];
var imageMap = new Map();

async function run_book() {
  let currentPageObj = await handle_cache();

  let tags = await get_api_requests("api/tags/" + currentPageObj["path"]);

  currentPageObj["tags"] = tags ? tags : [];

  const responseData = await get_api_requests(
    "api/images/" + currentPageObj["path"]
  );

  createBookInfoAndCover(currentPageObj, responseData[0]);

  responseData.forEach((element) => {
    createBookImageElement(element);
    //imageMap.set(element[1], element[0]);
  });

  document.getElementById("tagButton").onclick = function () {
    onClickTagButton(currentPageObj);
  };
}

function createBookImageElement(imgpath) {
  var imgEl = new Image();
  imgEl.src = "http://127.0.0.1:8000/load-image/" + imgpath;
  imgEl.alt = "img";

  var new_img_cover = document.createElement("div");
  new_img_cover.classList.add("img_box");
  new_img_cover.appendChild(imgEl);
  new_img_cover.onclick = function () {
    onClickBookImage(img_name);
  };

  document.getElementById("img_grid").appendChild(new_img_cover);
}

function onClickBookImage(img_name) {
  sessionStorage.setItem("currentPage", img_name);

  var image = imageMap.get(img_name);

  var overlay = document.getElementById("overlay");
  overlay.style.display = "grid";

  overlay.onclick = function () {
    onClickOverlayOff();
  };

  var imgBox = document.getElementById("image_overlay");

  var img_element = document.createElement("IMG");
  var img_src = "data:image/png;base64," + image;
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
        "data:image/png;base64," +
          imageMap.get(parseImageName(img_name, "left", imageMap.size()))
      );
    }
    if (event.key === "ArrowRight") {
      imgBox.childNodes[0].setAttribute(
        "src",
        "data:image/png;base64," +
          imageMap.get(parseImageName(img_name, "right", imageMap.size()))
      );
    }
  });
}

function onArrowPress(event, imgBox, imageName) {
  if (event.key === "ArrowLeft") {
    imgBox.childNodes[0].setAttribute(
      "src",
      "data:image/png;base64," +
        imageMap.get(parseImageName(imageName, "left", imageMap.size()))
    );
  }
  if (event.key === "ArrowRight") {
    imgBox.childNodes[0].setAttribute(
      "src",
      "data:image/png;base64," +
        imageMap.get(parseImageName(imageName, "right", imageMap.size()))
    );
  }
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

function createBookInfoAndCover(imgObj, coverpath) {
  var imageCover = new Image();
  imageCover.src = "http://127.0.0.1:8000/load-image/" + coverpath;
  imageCover.alt = imgObj["name"];
  //imageCover.style = "width: 50%; height: 50%;";
  var imageCoverElement = document.getElementById("imageCover");
  imageCoverElement.classList.add("img_cover");
  imageCoverElement.appendChild(imageCover);

  var imageTitle = document.getElementById("imageTitle");
  imageTitle.innerHTML = imgObj["name"];
  imageTitle.classList.add("Image-info-flex");

  var imageTags = document.getElementById("imageTags");
  imgObj["tags"].forEach((tag) => {
    var tagA = document.createElement("a");
    tagA.innerHTML = tag;
    tagA.classList.add("tags");
    imageTags.appendChild(tagA);
  });
}

function onClickTagButton(imgObj) {
  var tag = document.getElementById("tagField").value;
  if (tag != null && tag != "" && tag != " ") {
    url = "api/tags";
    data = { book: imgObj["path"], tag: tag.trim() };
    sendPutRequest(url, data);
    window.location.reload();
  }
}

document.getElementById("search_btn").onclick = function () {
  var inputQuery = document.getElementById("search_bar").value;
  window.location.href = "/search/" + inputQuery;
};

async function get_api_requests(path) {
  let result = [];
  try {
    const response = await fetch(`http://127.0.0.1:8000/${path}`);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    result = await response.json();
    console.log(result);
  } catch (error) {
    console.log(error);
  }

  return result;
}

function sendPutRequest(url, data) {
  const xhr = new XMLHttpRequest();
  xhr.open("PUT", "http://127.0.0.1:8000/" + url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onload = function () {
    if (xhr.status === 200) {
      console.log(xhr.responseText);
    } else {
      console.error(xhr.status, xhr.statusText);
    }
  };
  const jsonData = JSON.stringify(data);
  xhr.send(jsonData);
}

function getCookie(name) {
  var cookies = document.cookie.split("; ");
  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i].split("=");
    if (cookie[0] === name) {
      return JSON.parse(decodeURIComponent(cookie[1]));
    }
  }
  return null;
}

async function handle_cache() {
  let currentPageObj = JSON.parse(sessionStorage.getItem("currentBook"));
  if (!currentPageObj) {
    const uripath = window.location.pathname;
    const uriPathSegment = uripath.split("/");
    const book_id = uriPathSegment[uriPathSegment.length - 1];
    currentPageObj = await get_api_requests("api/book/" + book_id);
  }
  return currentPageObj;
}
