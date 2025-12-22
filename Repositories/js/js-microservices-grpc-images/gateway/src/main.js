// gateway/index.js
import express from 'express';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';

const app = express();
const PORT = 8080;

const SEARCH_SERVICE = 'search:8080';
const METADATA_SERVICE = 'metadata:8080';

function loadProto(path) {
    return grpc.loadPackageDefinition(
        protoLoader.loadSync(path, { keepCase: true })
    );
}

const searchProto = loadProto('proto/search.proto').search;
const metadataProto = loadProto('proto/metadata.proto').metadata;

const searchClient = new searchProto.Search(
    SEARCH_SERVICE,
    grpc.credentials.createInsecure()
);

const metadataClient = new metadataProto.Metadata(
    METADATA_SERVICE,
    grpc.credentials.createInsecure()
);

app.get('/images/search', (req, res) => {
    const kernel = Number(req.query.kernel ?? 3);
    const threshold = Number(req.query.threshold ?? 0.9);

    searchClient.Search(
        { kernel, threshold },
        (err, searchRes) => {
            if (err) {
                return res.status(503).json({ error: 'Search unavailable' });
            }

            if (!searchRes.imageIds.length) return res.json([]);

            metadataClient.Get(
                { imageIds: searchRes.imageIds },
                (err, metaRes) => {
                    if (err) {
                        return res.status(503).json({ error: 'Metadata unavailable' });
                    }
                    res.json(metaRes.images);
                }
            );
        }
    );
});

app.listen(PORT, '0.0.0.0', () =>
    console.log(`Gateway listening on 0.0.0.0:${PORT}`)
);
