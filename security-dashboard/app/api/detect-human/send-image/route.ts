// app/api/detect-human/send-image/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { writeFile, unlink } from 'fs/promises';
import path from 'path';
import { mkdir } from 'fs/promises';

// Make sure upload directory exists
const UPLOAD_DIR = path.join(process.cwd(), 'uploads');
try {
    await mkdir(UPLOAD_DIR, { recursive: true });
} catch (error) {
    console.error('Failed to create uploads directory', error);
}

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as File;
        const userId = formData.get('user_id') as string;
        const timestamp = formData.get('timestamp') as string;

        if (!file) {
            return NextResponse.json({ error: 'No image file uploaded' }, { status: 400 });
        }

        if (!userId) {
            return NextResponse.json({ error: 'Missing user_id parameter' }, { status: 400 });
        }

        // Create file path
        const bytes = await file.arrayBuffer();
        const buffer = Buffer.from(bytes);
        const filename = Date.now() + '-' + file.name;
        const filepath = path.join(UPLOAD_DIR, filename);

        // Save file temporarily
        await writeFile(filepath, buffer);

        // Send to Telegram
        const botToken = process.env.BOT_TOKEN;
        if (!botToken) {
            return NextResponse.json({ error: 'Bot token not configured' }, { status: 500 });
        }

        // Prepare form data for Telegram API
        const telegramFormData = new FormData();
        telegramFormData.append('chat_id', userId);
        telegramFormData.append('caption', `Alert! Human detected at ${timestamp || new Date().toISOString()}.`);
        telegramFormData.append('photo', new Blob([buffer]), filename);

        const endpoint = `https://api.telegram.org/bot${botToken}/sendPhoto`;

        // Send to Telegram
        const response = await fetch(endpoint, {
            method: 'POST',
            body: telegramFormData,
        });

        // Delete temp file
        await unlink(filepath);

        // Return response
        const result = await response.json();

        if (response.ok) {
            return NextResponse.json({
                status: 'Image Sent',
                telegram_response: result,
            });
        } else {
            return NextResponse.json(
                {
                    status: 'Failed to send image',
                    telegram_response: result,
                },
                { status: 500 }
            );
        }
    } catch (error) {
        console.error('Error processing request:', error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    }
}
