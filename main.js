const API = '/api';

function initDonorForm() {
    const form = document.querySelector('form');
    if (!form || form.id === 'donationForm') return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(`${API}/donors/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: data.name,
                    age: parseInt(data.age),
                    email: data.email,
                    phone: data.phone,
                    blood_type: data.blood_type,
                    address: data.address || '',
                    emergency_contact: data.emergency_contact || ''
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Registration failed');
            }

            alert('Donor registered successfully');
            window.location.href = '/donors';

        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

async function loadDonors() {
    const container = document.getElementById('donorsList');
    if (!container) return;

    try {
        const response = await fetch(`${API}/donors`);
        const donors = await response.json();

        if (!donors.length) {
            container.innerHTML = '<p>No donors registered yet.</p>';
            return;
        }

        container.innerHTML = donors.map(donor => `
            <div style="border:1px solid #ddd;padding:15px;margin:10px 0;border-radius:6px;">
                <h3>${donor.name}</h3>
                <p><strong>Blood Type:</strong> ${donor.blood_type}</p>
                <p><strong>Age:</strong> ${donor.age}</p>
                <p><strong>Email:</strong> ${donor.email}</p>
                <p><strong>Phone:</strong> ${donor.phone}</p>
                <button onclick="deleteDonor(${donor.id})"
                    style="background:red;color:white;padding:6px 12px;border:none;border-radius:4px;cursor:pointer;">
                    Delete
                </button>
            </div>
        `).join('');

    } catch (error) {
        container.innerHTML = '<p style="color:red;">Failed to load donors.</p>';
    }
}

async function deleteDonor(id) {
    if (!confirm("Are you sure you want to delete this donor?")) return;

    try {
        const response = await fetch(`${API}/donors/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Delete failed');
        }

        alert('Donor deleted successfully');
        loadDonors();

    } catch (error) {
        alert('Error: ' + error.message);
    }
}

window.deleteDonor = deleteDonor;

function initDonationForm() {
    const form = document.getElementById('donationForm');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(`${API}/donations/record`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    donor_id: parseInt(data.donor_id),
                    donation_date: data.donation_date,
                    quantity_ml: parseInt(data.quantity_ml),
                    hemoglobin: parseFloat(data.hemoglobin),
                    blood_pressure: data.blood_pressure,
                    notes: data.notes || ''
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to record donation');
            }

            alert('Donation recorded successfully');
            form.reset();

        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initDonorForm();
    loadDonors();
    initDonationForm();
});
