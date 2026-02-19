const API = "/api";

async function loadDonors() {

    const container = document.getElementById("donorsList");

    if (!container) return;

    try {

        const response = await fetch(`${API}/donors`);

        const donors = await response.json();

        if (!donors.length) {
            container.innerHTML = "<p>No donors found</p>";
            return;
        }

        container.innerHTML = donors.map(donor => `

            <div style="border:1px solid #ddd;padding:15px;margin:10px;border-radius:8px">

                <h3>${donor.name}</h3>

                <p><strong>Blood:</strong> ${donor.blood_type}</p>

                <p><strong>Age:</strong> ${donor.age}</p>

                <p><strong>Email:</strong> ${donor.email}</p>

                <p><strong>Phone:</strong> ${donor.phone}</p>

            </div>

        `).join("");

    } catch (error) {

        console.error(error);

        container.innerHTML =
            "<p style='color:red'>Failed loading donors</p>";
    }
}

document.addEventListener("DOMContentLoaded", loadDonors);
