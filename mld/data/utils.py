import torch


def lengths_to_mask(lengths):
    max_len = max(lengths)
    mask = torch.arange(max_len, device=lengths.device).expand(
        len(lengths), max_len) < lengths.unsqueeze(1)
    return mask


# padding to max length in one batch
def collate_tensors(batch):
    dims = batch[0].dim()
    max_size = [max([b.size(i) for b in batch]) for i in range(dims)]
    size = (len(batch), ) + tuple(max_size)
    canvas = batch[0].new_zeros(size=size)
    for i, b in enumerate(batch):
        sub_tensor = canvas[i]
        for d in range(dims):
            sub_tensor = sub_tensor.narrow(d, 0, b.size(d))
        sub_tensor.add_(b)
    return canvas


def all_collate(batch):
    notnone_batches = [b for b in batch if b is not None]
    databatch = [b["motion"] for b in notnone_batches]
    # labelbatch = [b['target'] for b in notnone_batches]
    if "lengths" in notnone_batches[0]:
        lenbatch = [b["lengths"] for b in notnone_batches]
    else:
        lenbatch = [len(b["inp"][0][0]) for b in notnone_batches]

    databatchTensor = collate_tensors(databatch)
    # labelbatchTensor = torch.as_tensor(labelbatch)
    lenbatchTensor = torch.as_tensor(lenbatch)
    maskbatchTensor = (lengths_to_mask(
        lenbatchTensor, databatchTensor.shape[-1]).unsqueeze(1).unsqueeze(1)
                       )  # unqueeze for broadcasting

    motion = databatchTensor
    cond = {"y": {"mask": maskbatchTensor, "lengths": lenbatchTensor}}

    if "text" in notnone_batches[0]:
        textbatch = [b["text"] for b in notnone_batches]
        cond["y"].update({"text": textbatch})

    # collate action textual names
    if "action_text" in notnone_batches[0]:
        action_text = [b["action_text"] for b in notnone_batches]
        cond["y"].update({"action_text": action_text})

    return motion, cond


# an adapter to our collate func
def mld_collate(batch):
    
    notnone_batches = [b for b in batch if b is not None]
    notnone_batches.sort(key=lambda x: x[3], reverse=True)
    # batch.sort(key=lambda x: x[3], reverse=True)
    adapted_batch = {
        "motion":
        collate_tensors([torch.tensor(b[4]).float() for b in notnone_batches]),
        "text": [b[2] for b in notnone_batches],
        "length": [b[5] for b in notnone_batches],
        "word_embs":
        collate_tensors([torch.tensor(b[0]).float() for b in notnone_batches]),
        "pos_ohot":
        collate_tensors([torch.tensor(b[1]).float() for b in notnone_batches]),
        "text_len":
        collate_tensors([torch.tensor(b[3]) for b in notnone_batches]),
        "tokens": [b[6] for b in notnone_batches],
        "retrieval_name": [b[7] for b in notnone_batches],
    }
    return adapted_batch


def mld_collate_vq_token(batch):
    notnone_batches = [b for b in batch if b is not None]
    notnone_batches.sort(key=lambda x: x[3], reverse=True)
    # batch.sort(key=lambda x: x[3], reverse=True)
    
    # for b in notnone_batches:
    #     print(torch.tensor(b[8]).shape)
    adapted_batch = {
        "motion":
        collate_tensors([torch.tensor(b[4]).float() for b in notnone_batches]),
        "text": [b[2] for b in notnone_batches],
        "length": [b[5] for b in notnone_batches],
        "word_embs":
        collate_tensors([torch.tensor(b[0]).float() for b in notnone_batches]),
        "pos_ohot":
        collate_tensors([torch.tensor(b[1]).float() for b in notnone_batches]),
        "text_len":
        collate_tensors([torch.tensor(b[3]) for b in notnone_batches]),
        "tokens": [b[6] for b in notnone_batches],
        "retrieval_name": [b[7] for b in notnone_batches],
        "motion_token": collate_tensors([torch.tensor(b[8]) for b in notnone_batches]),
        "motion_token_length": [b[9] for b in notnone_batches]

    }
    return adapted_batch


def vq_collate(batch):
    notnone_batches = [b for b in batch if b is not None]
    # notnone_batches.sort(key=lambda x: x[3], reverse=True)
    # batch.sort(key=lambda x: x[3], reverse=True)
    adapted_batch = {
        "motion":
        collate_tensors([torch.tensor(b[0]).float() for b in notnone_batches]),
        "name": [b[1] for b in notnone_batches], 
        "length": [b[2] for b in notnone_batches]
    }
    return adapted_batch


# an adapter to our collate func
def mld_motionx_collate(batch):
    notnone_batches = [b for b in batch if b is not None]
    notnone_batches.sort(key=lambda x: x[3], reverse=True)
    # batch.sort(key=lambda x: x[3], reverse=True)
    adapted_batch = {
        "motion":
        collate_tensors([torch.tensor(b[4]).float() for b in notnone_batches]),
        "text": [b[2] for b in notnone_batches],
        "length": [b[5] for b in notnone_batches],
        "word_embs":
        collate_tensors([torch.tensor(b[0]).float() for b in notnone_batches]),
        "pos_ohot":
        collate_tensors([torch.tensor(b[1]).float() for b in notnone_batches]),
        "text_len":
        collate_tensors([torch.tensor(b[3]) for b in notnone_batches]),
        "tokens": [b[6] for b in notnone_batches],
        "retrieval_name": [b[7] for b in notnone_batches], 
        "joint_mask": collate_tensors([torch.tensor(b[8]).float() for b in notnone_batches])
    }
    return adapted_batch


def mld_motionx_with_face_collate(batch):
    notnone_batches = [b for b in batch if b is not None]
    notnone_batches.sort(key=lambda x: x[3], reverse=True)
    # batch.sort(key=lambda x: x[3], reverse=True)
    adapted_batch = {
        "motion":
        collate_tensors([torch.tensor(b[4]).float() for b in notnone_batches]),
        "text": [b[2] for b in notnone_batches],
        "length": [b[5] for b in notnone_batches],
        "word_embs":
        collate_tensors([torch.tensor(b[0]).float() for b in notnone_batches]),
        "pos_ohot":
        collate_tensors([torch.tensor(b[1]).float() for b in notnone_batches]),
        "text_len":
        collate_tensors([torch.tensor(b[3]) for b in notnone_batches]),
        "tokens": [b[6] for b in notnone_batches],
        "retrieval_name": [b[7] for b in notnone_batches], 
        "joint_mask": collate_tensors([torch.tensor(b[8]).float() for b in notnone_batches]), 
        "face_motion":collate_tensors([torch.tensor(b[9]).float() for b in notnone_batches])
    }
    return adapted_batch

def mld_collate_text_all(batch):
    
    notnone_batches = [b for b in batch if b is not None]
    notnone_batches.sort(key=lambda x: x[3], reverse=True)
    # batch.sort(key=lambda x: x[3], reverse=True)
    adapted_batch = {
        "motion":
        collate_tensors([torch.tensor(b[4]).float() for b in notnone_batches]),
        "text": [b[2] for b in notnone_batches],
        "length": [b[5] for b in notnone_batches],
        "word_embs":
        collate_tensors([torch.tensor(b[0]).float() for b in notnone_batches]),
        "pos_ohot":
        collate_tensors([torch.tensor(b[1]).float() for b in notnone_batches]),
        "text_len":
        collate_tensors([torch.tensor(b[3]).float() for b in notnone_batches]),
        "tokens": [b[6] for b in notnone_batches],
        "body_text": [b[7] for b in notnone_batches],
        "hand_text": [b[8] for b in notnone_batches],
        "face_text": [b[9] for b in notnone_batches],

    }
    return adapted_batch

def a2m_collate(batch):

    databatch = [b[0] for b in batch]
    labelbatch = [b[1] for b in batch]
    lenbatch = [len(b[0][0][0]) for b in batch]
    labeltextbatch = [b[3] for b in batch]

    databatchTensor = collate_tensors(databatch)
    labelbatchTensor = torch.as_tensor(labelbatch).unsqueeze(1)
    lenbatchTensor = torch.as_tensor(lenbatch)

    maskbatchTensor = lengths_to_mask(lenbatchTensor)
    adapted_batch = {
        "motion": databatchTensor.permute(0, 3, 2, 1).flatten(start_dim=2),
        "action": labelbatchTensor,
        "action_text": labeltextbatch,
        "mask": maskbatchTensor,
        "length": lenbatchTensor
    }
    return adapted_batch
