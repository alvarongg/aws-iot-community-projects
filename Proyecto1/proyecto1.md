# Proyecto 1: Conexión Directa de Dispositivo IoT a AWS IoT Core

👋 ¡Bienvenido al primer proyecto de nuestro repositorio de AWS IoT Community Projects! 🚀

## 📋 Descripción

Este proyecto tiene como objetivo conectar de manera directa un dispositivo IoT al servicio de AWS IoT Core y almacenar los datos generados en un bucket de S3 para su posterior explotación. El despliegue de este proyecto se realiza de manera automática utilizando AWS CDK (Cloud Development Kit) en Python y la CLI de AWS para la descarga de certificados.

## 🎯 Objetivo del Proyecto

- **Conectar un dispositivo IoT**: Aprende a conectar tu dispositivo IoT al servicio de AWS IoT Core.
- **Almacenar datos en S3**: Configura un bucket de S3 para almacenar los datos recibidos del dispositivo IoT.
- **Automatización del despliegue**: Utiliza AWS CDK en Python para desplegar los recursos necesarios automáticamente.

## 🛠️ Requisitos

- **AWS CLI**: Asegúrate de tener instalada y configurada la AWS CLI. [Guía de instalación](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- **AWS CDK**: Instala AWS CDK para Python. [Guía de instalación](https://docs.aws.amazon.com/cdk/latest/guide/work-with-cdk-python.html)
- **Python 3.7+**: Asegúrate de tener Python 3.7 o superior instalado.

## 🚀 Cómo Empezar

1. **Clona el repositorio**:
    ```bash
    git clone https://github.com/tu-usuario/aws-iot-community-projects.git
    cd aws-iot-community-projects/proyecto-1
    ```

2. **Instala dependencias de Python**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows usa .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Despliega la infraestructura**:
    ```bash
    cdk deploy
    ```

4. **Descarga los certificados usando AWS CLI**:
    ```bash
    aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile cert.pem --public-key-outfile public.key --private-key-outfile private.key
    ```

## 📂 Estructura del Proyecto

- **/lib**: Contiene los stacks de AWS CDK.
- **/bin**: Contiene el archivo principal para la aplicación CDK.
- **/certs**: Directorio para almacenar los certificados descargados.

## 📬 Contacto

Para cualquier consulta o sugerencia, no dudes en contactarme por linkedin o abrir un issue en GitHub.

---

¡Esperamos que disfrutes experimentando con este proyecto y aprendiendo a conectar dispositivos IoT a AWS IoT Core! 🚀

✨ Happy hacking! ✨