from api.api_helpers import generate_image_by_prompt
from utils.helpers.randomize_seed import generate_random_15_digit_number
from api.open_websocket import open_websocket_connection
import json


def prompt_to_image(workflow, positve_prompt='', negative_prompt='', save_previews=False):
    prompt = json.loads(workflow)
    id_to_class_type = {id: details['class_type'] for id, details in prompt.items()}
    k_sampler = [key for key, value in id_to_class_type.items() if value == 'KSampler'][0]
    prompt.get(k_sampler)['inputs']['seed'] = generate_random_15_digit_number()

    postive_input_id = prompt.get(k_sampler)['inputs']['positive'][0]
    prompt.get(postive_input_id)['inputs']['text'] = positve_prompt

    if negative_prompt != '':
        negative_input_id = prompt.get(k_sampler)['inputs']['negative'][0]
        prompt.get(negative_input_id)['inputs']['text'] = positve_prompt

    generate_image_by_prompt(prompt, './output/', save_previews)


def prompt_to_image_mmq(workflow,input_img='',style_img='', positve_prompt='', negative_prompt='', save_previews=False):
    prompt = json.loads(workflow)
    id_to_class_type = {id: details['class_type'] for id, details in prompt.items()}
    image_loader_list = [key for key, value in id_to_class_type.items() if value == 'LoadImage']
    # k_sampler = [key for key, value in id_to_class_type.items() if value == 'KSampler'][0]
    # prompt.get(k_sampler)['inputs']['seed'] = generate_random_15_digit_number()

    if input_img != '':
        prompt.get(image_loader_list[0])['inputs']['image'] = input_img
    if style_img != '':
        prompt.get(image_loader_list[1])['inputs']['image'] = style_img


    # postive_input_id = prompt.get(k_sampler)['inputs']['positive'][0]
    # prompt.get(postive_input_id)['inputs']['text'] = positve_prompt

    # if negative_prompt != '':
    #   negative_input_id = prompt.get(k_sampler)['inputs']['negative'][0]
    #   prompt.get(negative_input_id)['inputs']['text'] = positve_prompt

    # prompt.get('10')['inputs']['seed'] = generate_random_15_digit_number()
    return generate_image_by_prompt(prompt, save_previews)
