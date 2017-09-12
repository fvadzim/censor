import artm
import glob
import os

import artm
import glob #module gives an opp to search for a file with a particular regex
import os



def get_batch_vectorizer(target_batches_folder, data_path):
    if not glob.glob(os.path.join(target_batches_folder, "*")):
        return artm.BatchVectorizer(data_path=data_path,
                                                data_format='vowpal_wabbit',
                                                collection_name=data_path+'_collection',
                                                target_folder=target_batches_folder)
    else:
        return artm.BatchVectorizer(data_path=target_batches_folder,
                                                data_format='batches')
def get_dict(target_batches_folder):
    dict_name = os.path.join(target_batches_folder, "dict.txt")
    dictionary = artm.Dictionary(name="dictionary")
    if not os.path.exists(dict_name):
        dictionary.gather(target_batches_folder)
        dictionary.save_text(dict_name)
    else:
        dictionary.load_text(dict_name)
    return dictionary

def print_top_words(model):
    for topic_name in model.topic_names:
        print(topic_name + ': ')
        if topic_named in last_tokens:
            for word in model.score_tracker["top_words"].last_tokens[topic_name]:
                print (word)
        else:
            print("free topic")
        print()

def generate_topic_names(topic_count, background_topic_count):

    background_topics, objective_topics, all_topics = [], [], []
    for i in range(topic_count):
        topic_name = ("background_topic_" + str(i)) if i < background_topic_count \
            else ("objective_topic_" + str(i - background_topic_count))
        all_topics.append(topic_name)
        if i < background_topic_count:
            background_topics.append(topic_name)
        else:
            objective_topics.append(topic_name)
    return all_topics, objective_topics, background_topics

def set_regularizers(model, devided, topic_names,  **regs):
    #print regs, regs['sparse_theta']
    all_topics, objective_topics, background_topics = topic_names
    if devided:
            if 'objective_sparse_phi' in regs:
                    model.regularizers.add(
                        artm.SmoothSparsePhiRegularizer(
                            name='objective_sparse_phi',
                            topic_names=objective_topics,
                            tau=regs['objective_sparse_phi']),
                        overwrite= True)
            if 'objective_sparse_theta' in regs:
                    model.regularizers.add(
                        artm.SmoothSparseThetaRegularizer(
                            name='objective_sparse_theta',
                            topic_names=objective_topics,
                            tau=regs['objective_sparse_theta']),
                        overwrite= True)
            if 'background_sparse_phi' in regs:
                    model.regularizers.add(
                        artm.SmoothSparsePhiRegularizer(
                            name='background_sparse_phi',
                            topic_names=background_topics,
                            tau=regs['background_sparse_phi']),
                        overwrite= True)
            if 'background_sparse_theta' in regs:
                    model.regularizers.add(
                        artm.SmoothSparseThetaRegularizer(
                            name='background_sparse_theta',
                            topic_names=background_topics,
                            tau=regs['background_sparse_theta']),
                        overwrite=True)
    else:
        if 'sparse_phi' in regs:
                    model.regularizers.add(
                        artm.SmoothSparsePhiRegularizer(
                            name='sparse_phi',
                            tau=regs['sparse_phi']),
                        overwrite=True)
        if 'sparse_theta' in regs:
                    model.regularizers.add(
                        artm.SmoothSparseThetaRegularizer(
                            name='sparse_theta',
                            tau=regs['sparse_theta']),
                        overwrite=True)
    if  'decorrelator_phi' in regs:
            if devided:
                model.regularizers.add(
                            artm.DecorrelatorPhiRegularizer(
                                name='decorrelator_phi',
                                topic_names=objective_topics,
                                tau=regs['decorrelator_phi']),
                            overwrite=True)
            else:
                model.regularizers.add(
                            artm.DecorrelatorPhiRegularizer(
                                name='decorrelator_phi',
                                tau=regs['decorrelator_phi']),
                            overwrite=True)

def set_scores(model, topic_names, devided=True,  **scores):
    #if not ('perplexity_score' in [score.name for
    #                               score in model.scores]):
    #    model.scores.add(PerplexityScore(name='perplexity_score'))
    all_topics, objective_topics ,background_topics = topic_names
    if 'top_tokens' in scores:
        model.scores.add(artm.TopTokensScore(
            name='top_tokens',
            num_tokens=scores['top_tokens']),
            overwrite= True)
    if 'top_tokens_extended' in scores:
        model.scores.add(artm.TopTokensScore(
            name='top_tokens_extended',
            num_tokens=scores['top_tokens_extended']),
            overwrite= True)

    if devided:
            if 'objective_sparsity_phi' in scores:
                    model.scores.add(
                        artm.SparsityPhiScore(
                            name='objective_sparsity_phi',
                            topic_names=objective_topics),
                        overwrite= True)
            if 'objective_sparsity_theta' in scores:
                    model.scores.add(
                        artm.SparsityThetaScore(
                            name='objective_sparsity_theta',
                            topic_names=objective_topics),
                        overwrite= True)
            if 'background_sparsity_phi' in scores:
                    model.scores.add(
                        artm.SparsityPhiScore(
                            name='background_sparsity_phi',
                            topic_names=background_topics),
                        overwrite= True)
            if 'background_sparsityity_theta' in scores:
                    model.scores.add(
                        artm.SparsityThetaScore(
                            name='background_sparsity_theta',
                            topic_names=background_topics),
                        overwrite=True)
    else:
        if 'sparsity_phi' in scores:
                    print ('if sparsity_phi in scores:')
                    model.scores.add(
                        artm.SparsityPhiScore(
                            name='sparsity_phi'),
                        overwrite=True)
        if 'sparsity_theta' in scores:
                    print ('sparsity_theta  in scores')
                    model.scores.add(
                        artm.SparsityThetaScore(
                            name='sparsity_theta'),
                        overwrite=True)


def get_scores(topic_names):
    # background_topics = (background_topics if background_topics else topics_amount//10)

    all_topics, objective_topics, background_topics = topic_names
    print("get_scores", all_topics)
    print("get scores : " , background_topics)
    print ("get_scores : " , objective_topics)

    scores_list=[]
    scores_list.append(artm.PerplexityScore(name='objective_perplexity_score',
                                            topic_names=objective_topics))
    scores_list.append(artm.SparsityPhiScore(name='objective_sparsity_phi',
                                             topic_names=objective_topics))
    scores_list.append(artm.SparsityThetaScore(name='objective_sparsity_theta',
                                               topic_names=objective_topics))

    scores_list.append(artm.PerplexityScore(name='perplexity_score',
                                            topic_names=all_topics))

    scores_list.append(artm.SparsityThetaScore(name='background_sparsity_theta',
                                               topic_names=background_topics))
    scores_list.append(artm.SparsityPhiScore(name='background_sparsity_phi',
                                               topic_names=background_topics))
    scores_list.append(artm.TopTokensScore(name="top_words",
                                              num_tokens=10, topic_names=objective_topics))
    return scores_list

batch_vectorizer=get_batch_vectorizer("bel_sites_batches", "bel_sites.txt")
dictionary=get_dict("bel_sites_batches")
T=50
topic_names = generate_topic_names(T, 2)
#print(topic_names[1])
devided_model = artm.ARTM(num_topics=T,
                          cache_theta=True,
                          reuse_theta=True,
                          theta_columns_naming="title",
                          seed=42,
                          scores=get_scores(topic_names),
                          num_document_passes=50,
                          topic_names=topic_names[0])

devided_model.initialize(dictionary)


set_regularizers(devided_model, devided=True,

                                             topic_names=topic_names,
                                             objective_sparse_phi=-0.75,
                                             objective_sparse_theta=-0.24,
                                             background_sparse_phi=+0.5,
                                             background_sparse_theta=+1.5,
                                             decorrelator_phi=-20)

set_scores(devided_model, topic_names=topic_names, devided=True, background_sparsity_phi=True,
                                        background_sparsity_theta=True)









print(devided_model.scores)
devided_model.fit_offline(batch_vectorizer=batch_vectorizer, \
                             num_collection_passes=5)
print(devided_model.regularizers)
#print(devided_model.score_tracker)
print(devided_model.score_tracker["top_words"].last_tokens)
for topic_name in devided_model.topic_names:
    print(topic_name + ': ')
    if topic_name in devided_model.score_tracker["top_words"].last_tokens:
        for word in devided_model.score_tracker["top_words"].last_tokens[topic_name]:
            print(word)
        print("\n")

print ("Perplexity:", devided_model.score_tracker["perplexity_score"].last_value)
print (devided_model.get_phi())
print(devided_model.get_theta())
#for i,raw in enumerate(devided_model.get_phi()):
#    print(i,' ',raw)
