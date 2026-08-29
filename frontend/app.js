const form = document.querySelector("#photo-form");
const fileInput = document.querySelector("#photo-input");
const titleInput = document.querySelector("#title-input");
const categoryInput = document.querySelector("#category-input");
const fileName = document.querySelector("#file-name");
const gallery = document.querySelector("#gallery");
const emptyState = document.querySelector("#empty-state");
const photoCount = document.querySelector("#photo-count");
const statusMessage = document.querySelector("#status-message");

function updateGalleryState() {
  const count = gallery.children.length;
  emptyState.hidden = count !== 0;
  photoCount.textContent = count === 1 ? "1 photo" : `${count} photos`;
}

fileInput.addEventListener("change", () => {
  fileName.textContent = fileInput.files[0]?.name || "No photo selected";
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const file = fileInput.files[0];

  if (!file) return;
  if (!file.type.startsWith("image/")) {
    statusMessage.textContent = "Please choose an image file.";
    return;
  }

  const photoUrl = URL.createObjectURL(file);
  const card = document.createElement("article");
  card.className = "card";

  const image = document.createElement("img");
  image.src = photoUrl;
  image.alt = titleInput.value;

  const content = document.createElement("div");
  content.className = "card-content";
  const title = document.createElement("h3");
  title.textContent = titleInput.value;
  const category = document.createElement("p");
  category.className = "category";
  category.textContent = categoryInput.value;
  const removeButton = document.createElement("button");
  removeButton.className = "delete-button";
  removeButton.type = "button";
  removeButton.textContent = "Delete";
  removeButton.addEventListener("click", () => {
    URL.revokeObjectURL(photoUrl);
    card.remove();
    updateGalleryState();
    statusMessage.textContent = "Photo removed from this local preview.";
  });

  content.append(title, category, removeButton);
  card.append(image, content);
  gallery.prepend(card);
  form.reset();
  fileName.textContent = "No photo selected";
  statusMessage.textContent = "Photo added to the local preview.";
  updateGalleryState();
});

updateGalleryState();
