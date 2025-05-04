from pyngrok import ngrok, conf
import time
import sys

def setup_ngrok():
    try:
        # Set your authtoken here
        NGROK_AUTHTOKEN = "2wdl1DHMy33tw5zCkmVwkLAszvP_6nqps5uGXLrhzLzFMMzPp"

        # Configure ngrok
        conf.get_default().auth_token = NGROK_AUTHTOKEN

        # Open a ngrok tunnel to the HTTP server
        public_url = ngrok.connect(8000)
        print(f'\nPublic URL: {public_url}\n')
        print('Share this URL with your friends to let them access your application.')
        print('Press Ctrl+C to stop the tunnel.\n')

        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down ngrok tunnel...")
        ngrok.kill()
    except Exception as e:
        error_msg = str(e)
        print("\nError: Authentication failed!")
        print("\nPlease follow these steps:")
        print("1. Go to https://dashboard.ngrok.com/signup and create an account")
        print("2. Check your email and click the verification link")
        print("3. After verifying, go to https://dashboard.ngrok.com/get-started/your-authtoken")
        print("4. Copy your new authtoken")
        print("5. Replace the NGROK_AUTHTOKEN in this script with your new token")
        print("\nIf you've already done these steps, make sure:")
        print("- You've verified your email address")
        print("- You're using the latest authtoken from your dashboard")
        print("- Your account is active")
        ngrok.kill()
        sys.exit(1)

if __name__ == "__main__":
    setup_ngrok() 