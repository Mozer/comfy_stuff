import os
from PIL import Image, ImageDraw
import glob

def create_image_pairs_and_masks():
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Supported image extensions (including WebP)
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
    
    # Get all image files in current directory with valid extensions
    image_files = []
    for ext in valid_extensions:
        image_files.extend(glob.glob(f'*_*{ext}'))
        image_files.extend(glob.glob(f'*_*{ext.upper()}'))  # Also check uppercase
    
    # Group images by their pair_id
    pairs = {}
    
    for image_file in image_files:
        try:
            # Extract filename without extension
            base_name = os.path.splitext(image_file)[0]
            
            # Split by underscore to get pair_id and side
            parts = base_name.split('_')
            if len(parts) != 2:
                continue
                
            pair_id = parts[0]
            side = parts[1]
            
            # Skip if side is not 0 or 1
            if side not in ['0', '1']:
                continue
            
            if pair_id not in pairs:
                pairs[pair_id] = {'left': None, 'right': None}
            
            if side == '0':
                pairs[pair_id]['left'] = image_file
            elif side == '1':
                pairs[pair_id]['right'] = image_file
                
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            continue
    
    # Process each pair
    for pair_id, images in pairs.items():
        left_path = images.get('left')
        right_path = images.get('right')
        
        if not left_path or not right_path:
            print(f"Warning: Incomplete pair for {pair_id}, skipping...")
            continue
        
        try:
            # Open images (supports WebP)
            left_img = Image.open(left_path).convert('RGB')
            right_img = Image.open(right_path).convert('RGB')
            
            # Resize right image to match left image height
            left_height = left_img.height
            left_width = left_img.width
            
            # Calculate new width for right image while maintaining aspect ratio
            aspect_ratio = right_img.width / right_img.height
            new_right_width = int(left_height * aspect_ratio)
            
            # Resize right image
            right_img_resized = right_img.resize((new_right_width, left_height), Image.Resampling.LANCZOS)
            
            # Create new image for concatenation
            total_width = left_width + new_right_width
            total_height = left_height
            combined_img = Image.new('RGB', (total_width, total_height))
            
            # Paste images
            combined_img.paste(left_img, (0, 0))
            combined_img.paste(right_img_resized, (left_width, 0))
            
            # Save combined image
            output_path = f'results/{pair_id}.jpg'
            combined_img.save(output_path, 'JPEG', quality=95)
            print(f"Created: {output_path}")
            
            # Create text file
            txt_path = f'results/{pair_id}.txt'
            with open(txt_path, 'w') as f:
                f.write("POV hand, zoom in, man's left hand is touching a woman's cheek")
            print(f"Created: {txt_path}")
            
            # Create mask for the combined image
            mask = Image.new('RGB', (total_width, total_height), color='black')
            draw = ImageDraw.Draw(mask)
            
            # Draw white rectangle on the right half
            white_rect = (total_width // 2, 0, total_width, total_height)
            draw.rectangle(white_rect, fill='white')
            
            # Save mask
            mask_filename = f'results/{pair_id}-masklabel.png'
            mask.save(mask_filename)
            print(f"Created mask: {mask_filename} ({total_width}x{total_height})")
            
            # Close images
            left_img.close()
            right_img.close()
            right_img_resized.close()
            combined_img.close()
            mask.close()
            
        except Exception as e:
            print(f"Error processing pair {pair_id}: {e}")
            continue

if __name__ == "__main__":
    create_image_pairs_and_masks()
    print("Processing complete!")