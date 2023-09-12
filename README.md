# OCI Generative AI Photo booth

A terraform script to start a photobooth gradio app using stable diffusion XL and cohere.ai to generate images based on cohere generated descriptions.

*You'll need access to GPUs to execute eveything.*

See the next video with all the steps.

## Requirements
- Terraform
- ssh-keygen

## Configuration

1. Follow the instructions to add the authentication to your tenant https://medium.com/@carlgira/install-oci-cli-and-configure-a-default-profile-802cc61abd4f.
2. Clone this repository:
    ```bash
    git clone https://github.com/carlgira/oci-genai-photobooth
    ```

3. Set three variables in your path. 
- The tenancy OCID, 
- The comparment OCID where the instance will be created.
- The number of instances to create
- The "Region Identifier" of region of your tenancy.
> **Note**: [More info on the list of available regions here.](https://docs.oracle.com/en-us/iaas/Content/General/Concepts/regions.htm)
- The cohere API key. You need to create an account in [cohere website](https://cohere.com/) and add a trial api key.

```bash
    export TF_VAR_tenancy_ocid='<tenancy-ocid>'
    export TF_VAR_compartment_ocid='<comparment-ocid>'
    export TF_VAR_region='<oci-region>'
    export TF_COHERE_API_KEY='<cohere-api-key>'
```

4. If you're using a Linux OS, you may need to execute the following command to to generate private key to access the instance.
```bash
    ssh-keygen -t rsa -b 2048 -N "" -f server.key
```

## Build

To build the terraform solution, simply execute: 

```bash
    terraform init
    terraform plan
    terraform apply
```

## ComfyUI
- Create a tunel to the machine like this.
```bash
ssh -i server.key -L 8188:localhost:8188 opc@<ip-address>
```

- Open comfyUI http://localhost:8188 

- From the GitHub repo drag and drop the images on top of ComfyUI to load the two pipelines
    - ComfyUI pipeline to detect correclty the colors of the chroma [test_chroma_pipeline.png](/comfyui/test_chroma_pipeline.png)
    - ComfyUI pipeline to to generate the photo booth image [photobooth_pipeline.png](/comfyui/photobooth_pipeline.png)

## Testing
Change the initial text of the "TextInput" node and upload an Image to the "Load Image" node and you can execute the pipeline to get the result.

## Acknowledgements

* **Authors** - [Carlos Giraldo](https://www.linkedin.com/in/carlos-giraldo-a79b073b/), Oracle
* **Last Updated Date** - September 12th, 2023
