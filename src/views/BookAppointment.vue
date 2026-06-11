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
      selectedSlot: "", // This will now hold the full selected object
      slots: []
    };
  },
  mounted() {
    this.fetchSlots();
  },
  methods: {
    fetchSlots() {
      fetch("https://e3pn66ir39.execute-api.us-east-1.amazonaws.com/prod/slots")
        .then(res => res.json())
        .then(data => {
          // Robust checking to handle API Gateway stringified bodies safely
          let rawSlots = data.body ? (typeof data.body === 'string' ? JSON.parse(data.body) : data.body) : data;
          
          if (Array.isArray(rawSlots)) {
            // MATCH YOUR DATABASE SCHEMA: filter by status === 'available'
            this.slots = rawSlots.filter(s => s.status === 'available');
          }
        })
        .catch(err => console.error("Error loading slots:", err));
    },
    submitAppointment() {
      if (!this.selectedSlot) {
        alert("Please select a valid time slot.");
        return;
      }

      // Payload matching what your database attributes expect
      const payload = {
        patientName: this.name,
        symptoms: this.symptoms,
        slotId: this.selectedSlot.slot_id,       // Pass the actual database identifier key
        timeLabel: this.selectedSlot.time_label   // Pass the display label string
      };

      fetch("https://e3pn66ir39.execute-api.us-east-1.amazonaws.com/prod/appointments", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload) // FIXED: Removed double-nesting stringification error
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
          this.fetchSlots(); // Automatically reload the unbooked dropdown variables
        })
        .catch(err => {
          console.error("Error booking appointment:", err);
          alert("Failed to book appointment. Make sure your target Lambda handles slot_id.");
        });
    }
  }
};
</script>
