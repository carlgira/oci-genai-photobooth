#!/bin/bash

main_function() {
USER='opc'

# Resize root partition
printf "fix\n" | parted ---pretend-input-tty /dev/sda print
VALUE=$(printf "unit s\nprint\n" | parted ---pretend-input-tty /dev/sda |  grep lvm | awk '{print $2}' | rev | cut -c2- | rev)
printf "rm 3\nIgnore\n" | parted ---pretend-input-tty /dev/sda
printf "unit s\nmkpart\n/dev/sda3\n\n$VALUE\n100%%\n" | parted ---pretend-input-tty /dev/sda
pvresize /dev/sda3
pvs
vgs
lvextend -l +100%FREE /dev/mapper/ocivolume-root
xfs_growfs -d /

dnf install wget git git-lfs jq python39 python39-devel.x86_64 python39-tkinter libsndfile rustc cargo unzip zip -y

alternatives --set python3 /usr/bin/python3.9

COHERE_KEY=`curl -L http://169.254.169.254/opc/v1/instance/ | jq -r '.metadata."cohere_api_key"'`

# ComfyUI
su -c "git clone https://github.com/comfyanonymous/ComfyUI.git /home/$USER/ComfyUI" $USER
su -c "git clone https://github.com/carlgira/oci-genai-photobooth /home/$USER/oci-genai-photobooth" $USER
su -c "cd /home/$USER/ComfyUI && python3 -m venv venv && source venv/bin/activate && pip install torch torchvision torchaudio opencv-python cohere --extra-index-url https://download.pytorch.org/whl/cu118 xformers && pip install -r requirements.txt && pip install rembg numpy==1.24 oci" $USER
su -c "cp /home/$USER/oci-genai-photobooth/comfyui/* /home/$USER/ComfyUI/custom_nodes" $USER
su -c "wget -O /home/$USER/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors" $USER
su -c "sed -i 's/COHERE_API_KEY/$COHERE_KEY/g' /home/$USER/oci-genai-photobooth/comfyui/start.sh" $USER
su -c "cp /home/$USER/oci-genai-photobooth/comfyui/start.sh /home/$USER/ComfyUI/start.sh" $USER

cat <<EOT >> /etc/systemd/system/comfyui.service
[Unit]
Description=systemd service start comfyui
[Service]
ExecStart=/bin/bash /home/$USER/ComfyUI/start.sh
User=$USER
[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload
systemctl enable comfyui.service
systemctl start comfyui.service

}

main_function 2>&1 >> /var/log/startup.log
