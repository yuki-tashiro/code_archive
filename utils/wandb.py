
# Colabでwandbにloginする際にコード
from google.colab import userdata
wandb_api_key = userdata.get('WANDB_API_KEY')
!wandb login $wandb_api_key

