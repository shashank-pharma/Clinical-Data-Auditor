# %% [markdown]
# Clinical trial data integrity ICHGCP requirement hai. 2 custom exceptions banao — PatientEligibilityError aur DataIntegrityError. Base class banao TrialParticipant jisme attributes hon — participant_id, age, weight, diagnosis. Child class banao AuditedParticipant(TrialParticipant) jisme method ho audit(min_age, max_age, required_diagnosis). Age range se bahar ho toh PatientEligibilityError, diagnosis match na kare toh DataIntegrityError raise karo. Logging se audit trail "trial_audit.txt" mein save karo. 4 participants test karo.

# %%
import logging
logging.basicConfig(
    filename="trial_audit.txt",
    level=logging.DEBUG,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

#building 2 cutom error classes
#1. patieneligibility error
class PatientEligibilityError(Exception):
    pass
#2. dataintegrity error
class DataIntegrityError(Exception):
    pass

#base class making
class TrialParticipants:
    def __init__(self, participant_id,age,weight,diagnosis):
        self.participant_id = participant_id
        self.age = age
        self.weight = weight
        self.diagnosis = diagnosis

    #how to display the data
    def __str__(self):
        return f"Participant ID: {self.participant_id} | Age: {self.age} |  Weight: {self.weight} |  Diagnosis: {self.diagnosis}"


#making the child class
class AuditedParticipants(TrialParticipants):
    def __init__(self, participant_id, age, weight, diagnosis):
        super().__init__(participant_id, age, weight, diagnosis)
     
    def audit(self,min_age,max_age,required_diagnosis):

        try:
            #checking the age
            if not min_age<=self.age<=max_age:
                raise PatientEligibilityError(f"Age {self.age} out of range {min_age}-{max_age}")

            # Diagnosis check
            if self.diagnosis != required_diagnosis:
                raise DataIntegrityError(
                    f"Diagnosis '{self.diagnosis}' != required '{required_diagnosis}'")

            msg =  f"{self.participant_id} — ELIGIBLE"
            print(f"{self.participant_id} is eligible for the trial")
            logging.info(msg)

        except PatientEligibilityError as e:
            print(f" Eligibility Error: {e}")
            logging.warning(f"{self.participant_id} — EligibilityError: {e}")

        except DataIntegrityError as e:
            print(f" Data Integrity Error: {e}")
            logging.warning(f"{self.participant_id} — DataIntegrityError: {e}")


#now we will be testing hypothetical participants
participants = [
    AuditedParticipants("P001", 30, 70, "Type2Diabetes"),
    AuditedParticipants("P002", 17, 65, "Type2Diabetes"),
    AuditedParticipants("P003", 45, 80, "Hypertension"),
    AuditedParticipants("P004", 50, 90, "Type2Diabetes")
]

for participant in participants:
    print(f" {participant}")
    participant.audit(min_age=18, max_age=65, required_diagnosis="Type2Diabetes")





