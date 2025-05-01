document.addEventListener("DOMContentLoaded", () => {
    console.log("DOMContentLoaded");
  
    // Écoute des événements SSE (Server-Sent Events)
    const source = new EventSource("/events");
  
    source.onmessage = (event) => {
      const data = JSON.parse(event.data);
  
      // Si c'est une mise à jour de l'état d'une note
      if (data.type === "update") {
        const checkbox = document.querySelector(`input[data-id="${data.id}"]`);
        if (checkbox) {
          checkbox.checked = data.done;
        }
      }
  
      // Si c'est une nouvelle note
      if (data.type === "new") {
        // Optionnel : recharger la page pour afficher la nouvelle note
        // window.location.reload();
        // Sinon, ajouter dynamiquement la nouvelle note
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
  
    // Gestion de l'état des cases à cocher comme d'habitude
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
  