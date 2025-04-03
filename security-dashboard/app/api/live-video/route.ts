import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'GET') {
        res.writeHead(200, {
            'Content-Type': 'video/mp4',
            'Transfer-Encoding': 'chunked',
        });

        // Simulate sending video chunks (replace this with actual video streaming logic)
        const interval = setInterval(() => {
            const chunk = Buffer.from('...'); // Replace with actual video chunk
            res.write(chunk);
        }, 100);

        req.on('close', () => {
            clearInterval(interval);
            res.end();
        });
    } else {
        res.status(405).json({ error: 'Method not allowed' });
    }
}
