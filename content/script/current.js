function createImageElement(img_obj) {
  var img_64 = img_obj[0];
  var img_name = img_obj[1];

  var img_element = document.createElement("IMG");
  var img_src = "data:image/jpeg;base64," + img_64;
  img_element.setAttribute("src", img_src);

  var new_img_cover = document.createElement("div");
  new_img_cover.classList.add("img_box");
  new_img_cover.appendChild(img_element);
  new_img_cover.onclick = function () {
    onClickImageCover(img_name);
  };

  document.getElementById("img_grid").appendChild(new_img_cover);
}

async function run_book() {
  var currentPage = sessionStorage.getItem("currentBook");

  let images = await eel.get_folder_images(currentPage)();

  images.forEach((element) => {
    createImageElement(element);
  });
}
