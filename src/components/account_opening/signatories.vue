<template>
  <div v-if="!isSubmitted">
    <label for="number_of_signatories">Number of signatories</label>
    <input
      v-model.number="numberOfSignatories"
      type="number"
      id="number_of_signatories"
      name="number_of_signatories"
      placeholder="Number of signatories"
      @input="updateSignatories"
      required
    />
    <div
      v-for="(signatory, index) in signatories"
      :key="index"
      class="form-group"
    >
      <h3>Signatory {{ index + 1 }}</h3>

      <label :for="'name_' + index">Name</label>
      <input
        v-model="signatory.name"
        type="text"
        :id="'name_' + index"
        :name="'name_' + index"
        placeholder="Enter name"
        required
      />

      <label :for="'id_no_' + index">National ID/Passport</label>
      <input
        v-model="signatory.id_no"
        type="text"
        :id="'id_no_' + index"
        :name="'id_no_' + index"
        placeholder="Enter National ID"
        required
      />

      <div class="file-input-wrapper">
        <label class="custom-file-label" :for="'file_' + index">
          Upload Signature
        </label>
        <input
          class="file-input"
          type="file"
          :id="'file_' + index"
          :name="'file_' + index"
          @change="handleFileUpload2($event, index)"
          required
        />
      </div>
    </div>

    <div v-if="missingData" class="error-message">
      Some Signatory data is missing
    </div>

    <button
      v-if="signatories.length >= 1"
      class="save-btn"
      @click.prevent="handleSubmit"
    >
      Save
    </button>
  </div>
  <div class="signatory-details" v-else>
    <div v-for="(sign, index) in signatories" :key="index">
      <h2>Signatory {{ index + 1 }}</h2>
      <p>Name: <span>{{ sign.name }}</span></p>
      <p>National ID: <span>{{ sign.id_no }}</span></p>
      <P>Signature: <span>{{ sign.file.name }}</span></P>
    </div>
  </div>
</template>

<script>
export default {
  name: "Account_Signatories",
  data() {
    return {
      numberOfSignatories: 0,
      signatories: [],
      missingData: false,
      isSubmitted: false,
    };
  },
  unmounted() {
  this.isSubmitted = false;
},
  methods: {
    handleFileUpload2(event, index) {
      const file = event.target.files[0];
      if (file) {
        this.signatories[index].file = file;
      }
    },
    updateSignatories() {
      const updatedNumber = this.numberOfSignatories || 0;
      if (updatedNumber > this.signatories.length) {
        // Add new signatories
        for (let i = this.signatories.length; i < updatedNumber; i++) {
          this.signatories.push({ name: "", id_no: "", file: null });
        }
      } else if (updatedNumber < this.signatories.length) {
        // Remove excess signatories
        this.signatories.splice(updatedNumber);
      }
    },
    handleSubmit() {
      const formDatasign = new FormData();

      this.signatories.forEach((signatory) => {
        switch (null) {
          case signatory.name:
          case signatory.id_no:
          case signatory.file:
            this.missingData = true;
            break;
          default:
            formDatasign.append("name", signatory.name);
            formDatasign.append("id_no", signatory.id_no);
            formDatasign.append("file", signatory.file);
        }
      });

      if (!this.missingData) {
        this.$emit("updateFormData", formDatasign);
        this.isSubmitted = true;
      }
    },
  },
};
</script>

<style scoped>
h3 {
  color: gold;
  margin-left: 5px;
}

h2 {
  color: white;
  margin-left: 5px;
}

input,
select,
.head {
  margin: 20px;
}

label {
  color: white;
  font-size: 15px;
  margin: 20px;
}

#number_of_signatories {
  background-color: rgb(0, 19, 31);
  color: white;
  border: 1px solid aqua;
  border-radius: 5px;
}

.file-input-wrapper {
  position: relative;
  display: inline-block;
}

.custom-file-label {
  display: inline-block;
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
}

.custom-file-label:hover {
  background-color: #0056b3;
}

.file-input {
  position: absolute;
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  z-index: -1;
}

.save-btn {
  background-color: #218bfc;
  color: white;
  border-radius: 5px;
  width: 200px;
  border: none;
  height: 50px;
  margin-left: 20px;
}
.error-message {
  margin-bottom: 10px;
}

p {
  color: aqua;
}
span {
  color: gold;
}
.signatory-details {
  margin-left: 20px;
}
</style>
