document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded");
  
    const source = new EventSource("/events");
  
    source.onmessage = (event) => {
      const data = JSON.parse(event.data);
  
      // Si mise à jour :
      if (data.type === "update") {
        const checkbox = document.querySelector(`input[data-id="${data.id}"]`);
        if (checkbox) {
          checkbox.checked = data.done;
        }
      }
  
      // Si nouvelle :
      if (data.type === "new") {

        const notesContainer = document.querySelector("#notes");
        const newNoteHTML = `
          <div class="note">
            <h2>${data.note.title}</h2>
            <p>${data.note.content}</p>
            <form method="POST">
              <label for="note-${data.note.id}">done</label>
              <input
                type="checkbox"
                data-id="${data.note.id}"
              >
            </form>
          </div>
        `;
        notesContainer.insertAdjacentHTML('beforeend', newNoteHTML);
      }
    };
  
    document.querySelectorAll(".note > form > input").forEach((element) => {
      element.addEventListener("change", (event) => {
        const done = element.checked;
        const id = element.dataset.id;
  
        fetch(`/api/notes/${id}/done`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ done }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.ok) {
              console.log("ok");
            } else {
              console.log(data.status, data);
            }
          });
      });
    });
  });
  