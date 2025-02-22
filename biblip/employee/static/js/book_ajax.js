$(document).ready(function () {
  $("#author, #genre").on("keydown", function (event) {
      if (event.key === "Enter") {
          event.preventDefault();
      }
  });

  let selectedAuthors = [];
  let selectedGenres = [];

  function buscarItens(url, inputId, resultsId, selectedList, listContainer, itemClass, removeClass, modelType) {
      $("#" + inputId).on("keyup", function (event) {
          let query = $(this).val();
          if (query.length < 1) {
              $("#" + resultsId).empty();
              return;
          }

          if (event.key === "Enter") {
              event.preventDefault();
              let selectedText = query.trim();

              if(selectedText === ""){
                return;
              }

              let selectedId = `new-${selectedText}-${modelType}`;

              if (!selectedList.some(item => item.id === selectedId)) {
                  selectedList.push({ id: selectedId, name: selectedText });

                  $("#" + listContainer).append(`
                      <li class="item">
                          ${selectedText} 
                          <button type="button" class="${removeClass}" data-value="${selectedId}">x</button>
                      </li>
                  `);
              }

              $("#" + inputId).val("");
              $("#" + resultsId).empty();
              return;
          }

          $.ajax({
              url: url,
              data: { q: query },
              dataType: "json",
              success: function (data) {
                  let list = $("#" + resultsId);
                  list.empty();
                  data.results.forEach(function (item, index) {
                      list.append(`<li class="${itemClass}" data-id="${data.id[index]}">${item}</li>`);
                  });
              }
          });
      });

      $("#" + resultsId).on("click", "." + itemClass, function () {
          let selectedText = $(this).data("name") || $(this).text();
          let selectedId = $(this).data("id") || `new-${selectedText}-${modelType}`;

          if (!selectedList.some(item => item.id === selectedId)) {
              selectedList.push({ id: selectedId, name: selectedText });

              $("#" + listContainer).append(`
                  <li class="item">
                      ${selectedText} 
                      <button type="button" class="${removeClass}" data-value="${selectedId}">x</button>
                  </li>
              `);
          }

          $("#" + inputId).val("");
          $("#" + resultsId).empty();
      });

      $("#" + listContainer).on("click", "." + removeClass, function () {
          let value = $(this).data("value");
          let index = selectedList.findIndex(item => item.id === value);
          if (index !== -1) {
              selectedList.splice(index, 1);
          }
          $(this).parent().remove();
      });

      let formAction = $("#form-action").val();
      let bookId = $("#book-id").val();

      if (formAction === "update" && bookId) {
          $.ajax({
              url: `/book/${bookId}/associated-datas`,
              method: "GET",
              dataType: "json",
              success: function (data) {
                  data.authors.forEach(author => {
                      if (!selectedAuthors.find(a => a.id === author.id)) {
                          selectedAuthors.push({ id: author.id, name: author.name });
                          $("#selected-authors").append(`
                              <li class="item">
                                  ${author.name}
                                  <button type="button" class="remove-author" data-value="${author.id}">x</button>
                              </li>
                          `);
                      }
                  });
                  
                  data.genres.forEach(genre => {
                      if (!selectedGenres.find(g => g.id === genre.id)) {
                          selectedGenres.push({ id: genre.id, name: genre.name });
                          $("#selected-genres").append(`
                              <li class="item">
                                  ${genre.name}
                                  <button type="button" class="remove-genre" data-value="${genre.id}">x</button>
                              </li>
                          `);
                      }
                  });
              },
              error: function () {
                  console.error("Erro ao buscar os dados do livro.");
              }
          });
      }
  }

  buscarItens(searchAuthorUrl, "author", "author-suggestions", selectedAuthors, "selected-authors", "selectable-author", "remove-author", "author");
  buscarItens(searchGenreUrl, "genre", "genre-suggestions", selectedGenres, "selected-genres", "selectable-genre", "remove-genre", "genre");

  let formAction = $("#form-action").val();
  let isUpdate = formAction === "update";

  $("#book-form").on("submit", function (event) {
      event.preventDefault();

      let formData = new FormData(this);
      let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
      let bookId = $("#book-id").val();

      selectedAuthors.forEach(author => {
          if (author.id.toString().startsWith("new-")) {
              formData.append("new_authors", author.name);
          } else {
              formData.append("book_author", author.id);
          }
      });
      
      selectedGenres.forEach(genre => {
          if (genre.id.toString().startsWith("new-")) {
              formData.append("new_genres", genre.name);
          } else {
              formData.append("book_genre", genre.id);
          }
      });

      let requestUrl = isUpdate ? `/book/${bookId}/update-associated-datas/` : '/book_create_ajax/';
      if (isUpdate) formData.append("book_id", bookId);

      fetch(requestUrl, {
          method: "POST",
          body: formData,
          headers: { "X-CSRFToken": csrfToken }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              window.location.href = data.redirect_url;
          } else if (data.errors) {
              alert("Erro: " + JSON.stringify(data.errors));
          } else {
              $("#book-form")[0].reset();
              $("#selected-authors, #selected-genres").empty();
              selectedAuthors = [];
              selectedGenres = [];
          }
      })
      .catch(error => console.error("Erro:", error));
  });

  var fileInput = document.querySelector('.file-input input');
  var fileDiv = document.querySelector('.file-input');

  fileInput.addEventListener('change', function () {
    if (fileInput.files.length > 0) {
        var fileURL = URL.createObjectURL(fileInput.files[0]);
        fileDiv.style.backgroundImage = `url('${fileURL}')`;
        fileDiv.style.backgroundSize = `cover`;
    }
  });

  var bookImageLink = document.querySelector('.file-input a');
  var bookImageUrl = bookImageLink.getAttribute('href');

  if(bookImageUrl && isUpdate){
    fileDiv.style.backgroundImage = `url('${bookImageUrl}')`;
    fileDiv.style.backgroundSize = `cover`;
  }
});
