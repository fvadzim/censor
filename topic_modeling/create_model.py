import artm
import glob
import os
def set_regularizers(model, devided=False,  **regs):
    #print regs, regs['sparse_theta']

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
                    print ('if sparse_phi in regs:')
                    model.regularizers.add(
                        artm.SmoothSparsePhiRegularizer(
                            name='sparse_phi',
                            tau=regs['sparse_phi']),
                        overwrite=True)
        if 'sparse_theta' in regs:
                    print ('sparse_theta  in regs')
                    model.regularizers.add(
                        artm.SmoothSparseThetaRegularizer(
                            name='sparse_theta',
                            tau=regs['sparse_theta']),
                        overwrite=True)
    if  'decorrelator_phi' in regs:
            print ('decorrelator  in regs')
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







source_file = "bel_sites.txt"
batches_folder = "bel_sites_batches"
if not glob.glob(os.path.join(batches_folder, "*")):
    batch_vectorizer = artm.BatchVectorizer(data_path=source_file,
                                            data_format="vowpal_wabbit",
                                            target_folder=batches_folder,
                                            batch_size=100)
else:
    batch_vectorizer = artm.BatchVectorizer(data_path=batches_folder,
                                            data_format='batches')

dict_name = os.path.join(batches_folder, "dict.txt")
dictionary = artm.Dictionary(name="dictionary")
if not os.path.exists(dict_name):
    dictionary.gather(batches_folder)
    dictionary.save_text(dict_name)
else:
    dictionary.load_text(dict_name)

T = 200   # количество тем
all_topics = ["topic_" + str(i) for i in range(T)]
scores_list = []
scores_list.append(artm.PerplexityScore(name='PerplexityScore'))  # перплексия (перенормированное правдоподобие)
scores_list.append(artm.SparsityPhiScore(name='SparsityPhiScore', class_id="@content"))   # разреженность Phi
scores_list.append(artm.SparsityThetaScore(name='SparsityThetaScore'))   # разреженность Theta
scores_list.append(artm.TopTokensScore(name="top_words",
                                          num_tokens=15, class_id="@content"))  # для печати наиболее вероятных терминов темы
model_artm = artm.ARTM(num_topics=T,  # число тем
                       class_ids={"@content":1, "@category_text":1, "@title":1},   # число после названия модальностей - это их веса
                       num_document_passes=10,   # сколько делать проходов по документу
                       cache_theta=True,   # хранить или нет глоабльную матрицу Theta
                       reuse_theta=False,   # если Theta хранится, нужно ли ее вновь инициализировать при каждом проходе
                       theta_columns_naming="theta_column",   # как именовать столбцы в матрице Theta
                       seed=789,   # random seed
                       scores=scores_list)  # метрики качества
model_artm.topic_names = all_topics
model_artm.initialize(dictionary)
set_regularizers(model_artm, devided=False, sparse_phi=-0.5,
                                            sparse_theta=-4.0,
                                            decorrelator_phi=10)


model_artm.fit_offline(batch_vectorizer=batch_vectorizer, \
                             num_collection_passes=3)

for topic_name in all_topics:
    print(topic_name + ': ')
    if topic_name in model_artm.score_tracker["top_words"].last_tokens:
        for word in model_artm.score_tracker["top_words"].last_tokens[topic_name]:
            print(word)
        print("\n")

print ("Perplexity:", model_artm.score_tracker["PerplexityScore"].last_value)
print(model_artm.get_phi())
for i,raw in enumerate(model_artm.get_phi()):
    print(i,' ',raw)

print(
model_artm.score_tracker["top_words"].__dict__,
model_artm.score_tracker["top_words"].last_tokens)
