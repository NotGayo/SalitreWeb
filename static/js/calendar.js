/* ===== código que ya tienes (pintar calendario, elegir hora, etc.) ===== */

/* ===== NUEVO: enviar a nuestra API justo antes de FormSubmit ===== */
document.getElementById("reservationForm").addEventListener("submit", async (e) => {
    const form = e.target;

    const payload = {
        "Nombre": form.Nombre.value.trim(),
        "Teléfono": form.Teléfono.value.trim(),
        "Email": form.Email.value.trim(),
        "Personas": form.Personas.value,
        "Fecha y hora": document.getElementById("selectedDateTime").value,
        "Notas": form.Notas.value.trim()
    };

    try {
        const r = await fetch("/api/reservas", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload)
        });
        if (!r.ok) throw new Error("Error guardando en BBDD");
    } catch (err) {
        console.error(err);
    }
    /* dejamos que el submit continúe → FormSubmit enviará el e-mail */
});