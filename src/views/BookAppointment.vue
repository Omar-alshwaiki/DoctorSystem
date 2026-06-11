<template>
  <div>
    <nav class="navbar navbar-light bg-white shadow-sm mb-4">
      <div class="container d-flex justify-content-between align-items-center">
        <span class="fw-bold fs-5">Doctor Appointments</span>
        <router-link to="/appointments" class="btn btn-outline-primary">⇆ Switch Page</router-link>
      </div>
    </nav>

    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow p-5" style="width: 100%; max-width: 700px;">
        <h2 class="text-center mb-4 text-primary">Book an Appointment</h2>
        <form class="row g-3" @submit.prevent="submitAppointment">
          <div class="col-12">
            <input v-model="name" type="text" class="form-control" placeholder="Your Name" required />
          </div>
          <div class="col-12">
            <input v-model="symptoms" type="text" class="form-control" placeholder="Symptoms" required />
          </div>
          <div class="col-12">
            <select v-model="selectedSlot" class="form-select" required>
              <option disabled value="">Select a Time Slot</option>
              <option v-for="slot in slots" :key="slot.slot_id" :value="slot">
                {{ slot.time_label }}
              </option>
            </select>
          </div>
          <div class="col-12">
            <button type="submit" class="btn btn-primary w-100">Book</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BookAppointment",
  data() {
    return {
      name: "",
      symptoms: "",
      selectedSlot: "",
      slots: []
    };
  },
  mounted() {
    this.fetchSlots();
  },
  methods: {
    fetchSlots() {
      fetch("https://YOUR_API_GATEWAY_URL/prod/slots")
        .then(res => res.json())
        .then(data => {
          let rawSlots = data.body ? (typeof data.body === 'string' ? JSON.parse(data.body) : data.body) : data;
          if (Array.isArray(rawSlots)) {
            // Filter using your correct string value flag
            this.slots = rawSlots.filter(s => s.status === 'available');
          }
        })
        .catch(err => console.error("Error loading slots:", err));
    },
    submitAppointment() {
      if (!this.selectedSlot) {
        alert("Please select a time slot.");
        return;
      }

      const payload = {
        patientName: this.name,
        symptoms: this.symptoms,
        slotId: this.selectedSlot.slot_id,
        timeLabel: this.selectedSlot.time_label
      };

      fetch("https://YOUR_API_GATEWAY_URL/prod/appointments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(async res => {
          if (!res.ok) {
            const errText = await res.text();
            throw new Error(errText);
          }
          return res.json();
        })
        .then(() => {
          alert("Appointment booked!");
          this.name = "";
          this.symptoms = "";
          this.selectedSlot = "";
          this.fetchSlots();
        })
        .catch(err => {
          console.error("Error booking appointment:", err);
          alert("Failed to book appointment.");
        });
    }
  }
};
</script>
