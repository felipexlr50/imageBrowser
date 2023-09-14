async function run() {
  const responseData = await get_api_requests("/api/images/latest");
  console.log(responseData);

  responseData.forEach((element) => {
    createImageElement(element);
  });
}

function createImageElement(img_obj) {
  var img_name = img_obj["name"];
  var linkEl = document.createElement("a");
  linkEl.href = "/book/" + img_obj["id"];
  linkEl.onclick = function () {
    // Set data in localStorage here
    onClickImageCover(img_obj);

    // Allow the default link behavior to proceed
    return true;
  };
  var imgEl = new Image();
  imgEl.src = "http://127.0.0.1:8000/load-image/" + img_obj["path"];
  imgEl.alt = img_name;
  //imgEl.style = "width: 100%; height: 100%;";

  var img_name_element = document.createTextNode(img_name);

  var new_img_cover = document.createElement("div");
  new_img_cover.classList.add("img_box");
  linkEl.appendChild(imgEl);
  new_img_cover.appendChild(linkEl);
  new_img_cover.appendChild(img_name_element);
  // new_img_cover.onclick = function () {
  //   onClickImageCover(img_obj);
  // };

  document.getElementById("img_grid").appendChild(new_img_cover);
}

function onClickImageCover(img_obj) {
  sessionStorage.setItem("currentBook", JSON.stringify(img_obj));
  document.cookie =
    "currentBook=" + encodeURIComponent(JSON.stringify(img_obj)) + "; path=/";
  // window.location.href = "/book/" + img_obj["id"];
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
